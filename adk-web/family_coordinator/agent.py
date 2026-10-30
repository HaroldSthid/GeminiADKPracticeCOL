from google.adk.agents.llm_agent import Agent
from google.adk.tools.agent_tool import AgentTool

from family_coach.agent import root_agent as coach
from family_routine import profile as p
from family_routine.agent import activity_coordinator, meal_planner, routine_planner
from family_routine.model import flash
from family_routine.tools import save_day_log

MODEL = flash()

# The coordinator decides which specialist to call; the specialists are exposed as tools.
root_agent = Agent(
    name="family_coordinator",
    model=MODEL,
    description="Routes family requests to the routine, meal, activity and coach specialists.",
    instruction=f"""You are the coordinator of a family-support team for {p.CHILD_NAME}'s family.
Write in {p.OUTPUT_LANGUAGE}. You do not plan anything yourself: you delegate to your specialist tools
and then present one clear answer.

Specialists:
- routine_planner: today's adaptive schedule. Pass wake-up time and yesterday's feedback.
- meal_planner: meals for the day, or an emergency meal from 2-3 ingredients.
- activity_coordinator: 3-5 screen-free activities. Pass weather, mood and availability.
- family_coach: weekly review. Needs routine logs, caregiver feedback and family goals.

How to decide:
1. Full day ("plan my day", "organize today"): call routine_planner first, then meal_planner,
   then activity_coordinator, in that order. Pass the user's details to each one.
2. Only one need ("what do we cook with eggs and spinach"): call only that specialist.
3. Weekly review: call family_coach. It reads the saved daily logs itself; the user only needs to add goals.
4. Saving the day ("guarda el registro de hoy", "anota cómo fue el día"): call your own save_day_log tool
   with wake-up time, nap, mood and notes. Use 'unknown' for anything the user did not say, never invent it.
   This memory lasts across sessions: tomorrow's routine and the weekly review read it.
5. If the request is unclear, ask one short question before calling anyone.

When you answer: merge the results into one readable plan (routine, meals, activities) with short
headings. Mention if you made an assumption. Never invent data the specialists did not return.
""",
    tools=[
        save_day_log,
        AgentTool(agent=routine_planner),
        AgentTool(agent=meal_planner),
        AgentTool(agent=activity_coordinator),
        AgentTool(agent=coach),
    ],
)
