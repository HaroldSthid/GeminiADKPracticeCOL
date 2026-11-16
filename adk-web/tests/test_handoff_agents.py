import pytest
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.tools.agent_tool import AgentTool

from handoff_kit.agents import build_chain, build_team
from handoff_kit.domains import load_domain

DOMAIN = load_domain("company_orders")
MODEL = "gemini-flash-latest"


@pytest.fixture(scope="module")
def team():
    return build_team(DOMAIN, MODEL)


def agent_tools(coordinator):
    return {t.agent.name: t.agent for t in coordinator.tools if isinstance(t, AgentTool)}


def test_coordinator_exposes_each_stage_and_coach_as_agent_tools(team):
    coordinator, coach = team
    tools = agent_tools(coordinator)
    assert set(tools) == {s.key for s in DOMAIN.stages} | {coach.name}
    assert not any(isinstance(a, SequentialAgent) for a in tools.values())
    assert any(getattr(t, "__name__", "") == "save_log" for t in coordinator.tools)
    assert coordinator.name == "ops_coordinator"


def test_stage_agents_use_output_key(team):
    tools = agent_tools(team[0])
    for stage in DOMAIN.stages:
        assert tools[stage.key].output_key == stage.key


def test_later_stages_read_previous_state_placeholders(team):
    tools = agent_tools(team[0])
    keys = [s.key for s in DOMAIN.stages]
    assert "{" + keys[0] + "?}" not in tools[keys[0]].instruction
    assert "{" + keys[0] + "?}" in tools[keys[1]].instruction
    assert "{" + keys[0] + "?}" in tools[keys[2]].instruction
    assert "{" + keys[1] + "?}" in tools[keys[2]].instruction


def test_first_stage_reads_logs_others_do_not(team):
    tools = agent_tools(team[0])
    first, second = DOMAIN.stages[0].key, DOMAIN.stages[1].key
    assert [t.__name__ for t in tools[first].tools] == ["get_recent_logs"]
    assert "days=2" in tools[first].instruction
    assert not tools[second].tools


def test_forbidden_inventions_context_and_language_in_every_stage(team):
    tools = agent_tools(team[0])
    for stage in DOMAIN.stages:
        text = tools[stage.key].instruction
        assert DOMAIN.forbidden_inventions in text
        assert DOMAIN.output_language in text
        for fact in DOMAIN.context.values():
            assert fact in text


def test_stage_chain_is_a_sequential_agent_over_the_stage_agents():
    chain = build_chain(DOMAIN, MODEL)
    assert isinstance(chain, SequentialAgent)
    assert [a.name for a in chain.sub_agents] == [s.key for s in DOMAIN.stages]
    assert [a.output_key for a in chain.sub_agents] == [s.key for s in DOMAIN.stages]


def test_coach_has_grounding_rules_and_goal(team):
    _, coach = team
    text = coach.instruction
    assert DOMAIN.coach_goal_hint in text
    assert '"progress"' in text and "pattern" in text
    assert "hypothesis" in text
    assert "fewer than 4" in text
    assert "superlatives" in text
    assert "get_recent_logs" in text and "days=7" in text
    assert [t.__name__ for t in coach.tools] == ["get_recent_logs"]


def test_every_stage_keeps_assumptions_out_of_external_messages(team):
    tools = agent_tools(team[0])
    for stage in DOMAIN.stages:
        text = tools[stage.key].instruction
        assert "Never present an assumption as a fact" in text
        assert "pending confirmation" in text


def test_coordinator_keeps_assumptions_labeled_when_merging(team):
    coordinator, _ = team
    assert "Never present an assumption as a fact" in coordinator.instruction


def test_coordinator_saves_the_identifier_exactly_as_the_user_wrote_it(team):
    coordinator, _ = team
    text = coordinator.instruction
    assert f"the {DOMAIN.subject_label} identifier exactly as the user wrote it" in text
    assert "never add a prefix" in text
    assert "change the case" in text


def test_coordinator_saves_only_the_bare_identifier_without_the_label_word(team):
    # Live failure: "ticket 520, cliente Ortiz" was saved as "ticket 520" while the seed uses "481".
    coordinator, _ = team
    text = coordinator.instruction
    label = DOMAIN.subject_label
    assert f'without the word "{label}"' in text
    assert f'from "{label} 520" save only 520' in text


def test_agents_never_name_a_person_team_or_area_the_company_did_not_mention(team):
    # Live failure: the refund was routed to "the commercial/administrative area", which nobody said.
    coordinator, _ = team
    rule = "Never name a person, team or area that the company context and your instructions do not mention"
    assert rule in coordinator.instruction
    for stage in DOMAIN.stages:
        assert rule in agent_tools(coordinator)[stage.key].instruction


def test_coordinator_instruction_has_no_braces_that_adk_would_read_as_variables(team):
    coordinator, _ = team
    assert "{" not in coordinator.instruction and "}" not in coordinator.instruction


def test_coordinator_instruction_mentions_every_stage_key(team):
    coordinator, coach = team
    for stage in DOMAIN.stages:
        assert stage.key in coordinator.instruction
    assert coach.name in coordinator.instruction
    assert "save_log" in coordinator.instruction
    assert "unknown" in coordinator.instruction
