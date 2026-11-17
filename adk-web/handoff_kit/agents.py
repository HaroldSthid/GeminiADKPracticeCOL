"""Builds the coordinator + stage chain + coach team from a Domain."""

from google.adk.agents.llm_agent import Agent
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools.agent_tool import AgentTool

from .domain import Domain, Stage
from .tools import build_tools


def _context_block(domain: Domain) -> str:
    return "\n".join(f"- {label}: {fact}" for label, fact in domain.context.items())


def _stage_instruction(domain: Domain, index: int) -> str:
    stage: Stage = domain.stages[index]
    previous = domain.stages[:index]
    lines = [
        f"You are the {stage.title} area of the company case '{domain.name}'. Write in {domain.output_language}.",
        "",
        "Company context:",
        _context_block(domain),
        "",
        f"You receive: {stage.receives}",
        f"You deliver: {stage.delivers}",
        "",
    ]
    if index == 0:
        lines += [
            "First call get_recent_logs with days=2 to learn what happened in the previous days.",
            "The user's message always overrides the saved logs.",
            "If a saved log describes a similar case (same kind of request, same channel or the same lateness),",
            "add one line to your handoff note that cites it with its identifier and date exactly as saved.",
            "Never claim a similarity the saved logs do not show. If none is similar, add nothing.",
            "",
        ]
    for prev in previous:
        lines += [f"Output of the {prev.title} area ({prev.key}), already produced:", "{" + prev.key + "?}", ""]
    if previous:
        lines += ["If an earlier output is empty, say so and work only with what the user provided.", ""]
    lines += [
        "Your job rules:",
        stage.instruction,
        "",
        "Never invent anything:",
        domain.forbidden_inventions,
        "If a detail is missing, say it is missing and state the assumption you made.",
        "Never present an assumption as a fact, least of all in a message addressed to someone outside",
        "the team (for example a customer): word it as pending confirmation, never as something certain.",
        "Never name a person, team or area that the company context and your instructions do not mention:",
        "when someone must decide or act and nobody is named, say 'a person' and flag it.",
    ]
    return "\n".join(lines)


def build_stage_agents(domain: Domain, model, get_recent_logs=None) -> list[Agent]:
    if get_recent_logs is None:
        _, get_recent_logs = build_tools(domain)
    agents = []
    for index, stage in enumerate(domain.stages):
        agents.append(
            Agent(
                name=stage.key,
                model=model,
                description=f"{stage.title}: receives {stage.receives} and delivers {stage.delivers}.",
                instruction=_stage_instruction(domain, index),
                tools=[get_recent_logs] if index == 0 else [],
                output_key=stage.key,
            )
        )
    return agents


def build_chain(domain: Domain, model) -> SequentialAgent:
    """The stages as one sequential chain (stage outputs flow through session state)."""
    return SequentialAgent(
        name=f"{domain.stages[0].key}_to_{domain.stages[-1].key}",
        sub_agents=build_stage_agents(domain, model),
        description=" -> ".join(s.title for s in domain.stages),
    )


def _coach_instruction(domain: Domain) -> str:
    return f"""You are the weekly coach for the company case '{domain.name}'. Write in {domain.output_language}.

Company context:
{_context_block(domain)}

First call get_recent_logs with days=7 to read the saved logs.
The user may add feedback or goals; if the goals are missing, ask for them.
If there are no saved logs and the user gave none, say so and ask for them before analyzing.
What you look for: {domain.coach_goal_hint}

Then:
1. Compare the logs with the goals. Say "progress" only if the days improve over time.
   If they alternate, call it a pattern, not progress.
2. Name 1-2 patterns or successes. Cite the dates and values from the logs.
3. Name challenges only if the logs show them. If none, write that the logs show no clear challenge.
   Never invent a cause or a detail the logs do not state. If you infer a cause, say it is a hypothesis.
4. Give 2-3 actionable recommendations for the UPCOMING week.
5. If fewer than 4 days are logged, say the analysis rests on few days.
Keep a measured tone: no superlatives, no praise that the data does not support.

Never invent anything:
{domain.forbidden_inventions}

Format: 'Positive findings', 'Challenges', 'Recommendations for next week' (translated into the output language).
"""


def _coordinator_instruction(domain: Domain, coach_name: str) -> str:
    stage_lines = "\n".join(
        f"- {s.key}: {s.title}. Receives {s.receives}. Delivers {s.delivers}." for s in domain.stages
    )
    order = ", then ".join(s.key for s in domain.stages)
    return f"""You are '{domain.coordinator_name}', the coordinator of the company case '{domain.name}'.
{domain.coordinator_role}
Write in {domain.output_language}. You do not do the work yourself: you delegate to your tools
and then present one clear answer.

Company context:
{_context_block(domain)}

Specialists:
{stage_lines}
- {coach_name}: weekly review of the saved logs. The user only needs to add goals.

How to decide:
1. Full request: call {order}, in that order. Pass the user's details to each one.
2. Only one need: call only that stage.
3. Weekly review: call {coach_name}. It reads the saved logs itself.
4. "Save the log": call your own save_log tool with the {domain.subject_label} and the details.
   Save the {domain.subject_label} identifier exactly as the user wrote it: never add a prefix,
   change the case or reformat it, so the same {domain.subject_label} is always logged the same way.
   Save only the bare identifier (its number or code) without the word "{domain.subject_label}" or any
   other label in front: from "{domain.subject_label} 520" save only 520.
   Use 'unknown' for anything the user did not say, never invent it.
   This memory lasts across sessions: the first stage and the weekly review read it.
5. If the request is unclear, ask one short question before calling anyone.

When you answer: merge the results into one readable answer with short headings.
If a specialist cites a similar earlier case from the saved logs, keep that line in your answer
with its identifier and date exactly as given. Never drop it and never add a similarity yourself.
State every assumption you made. Never present an assumption as a fact, and never invent data
the specialists did not return.
Never name a person, team or area that the company context and your instructions do not mention: when someone must decide or act and nobody is named, say 'a person'.
{domain.forbidden_inventions}
"""


def build_team(domain: Domain, model) -> tuple[Agent, Agent]:
    """Returns (coordinator, coach). The model is a parameter so tests never touch the network."""
    save_log, get_recent_logs = build_tools(domain)
    stages = build_stage_agents(domain, model, get_recent_logs)
    coach = Agent(
        name="weekly_coach",
        model=model,
        description="Analyzes the past week of logs and recommends adjustments.",
        instruction=_coach_instruction(domain),
        tools=[get_recent_logs],
    )
    coordinator = Agent(
        name="ops_coordinator",
        model=model,
        description=f"Routes requests to {', '.join(s.title for s in domain.stages)} and the weekly coach.",
        instruction=_coordinator_instruction(domain, coach.name),
        tools=[save_log, *(AgentTool(agent=a) for a in stages), AgentTool(agent=coach)],
    )
    return coordinator, coach
