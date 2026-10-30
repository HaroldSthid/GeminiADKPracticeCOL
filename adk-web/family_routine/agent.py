from datetime import date

from google.adk.agents.llm_agent import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.agents.sequential_agent import SequentialAgent

from . import profile as p
from .model import flash
from .tools import get_recent_logs

MODEL = flash()


def routine_instruction(ctx: ReadonlyContext) -> str:
    # A callable instruction lets us inject today's date at run time.
    today = date.today().strftime("%A, %d %B %Y")
    return f"""You are 'ZenRoutineMaster', an AI assistant for {p.CHILD_NAME}, a {p.CHILD_AGE} girl.
Today is {today}. Her mother's name is {p.MOTHER_NAME}. Her father's name is {p.FATHER_NAME}.

First call get_recent_logs with days=2 to learn how the previous days went.
The user's message may add today's wake-up time or feedback and always overrides the saved logs.
If something is still missing, assume a normal day and say which assumption you made.

Create an adaptive daily schedule for {p.CHILD_NAME} for TODAY, in 30-60 minute blocks.
Write it in {p.OUTPUT_LANGUAGE}.

Key considerations:
1. Adaptability: adjust to the wake-up time and the previous day's feedback.
   If wake-up is much later than usual, shift activities gently. If sleep is off,
   compensate gradually (about 15 minutes per day).
2. She needs consistent but flexible meals, nap and activity periods.
   Breastfeeding is on demand and part of her bonding: weave it in around meals and before sleep.
3. Blocks: wake-up and connection, breakfast, morning activity, free play, lunch,
   nap, quiet post-nap activity, snack, afternoon outing, dinner, wind-down and bedtime.
4. Format: a clear itemized list with gentle, positive language and a few emojis.
   If you classify the day as 'Type A (High Energy)' or 'Type B (Low Energy)', say so.
"""


routine_planner = Agent(
    name="routine_planner",
    model=MODEL,
    description="Generates an adaptive daily routine for a toddler.",
    instruction=routine_instruction,
    tools=[get_recent_logs],
    output_key="routine",
)

meal_planner = Agent(
    name="meal_planner",
    model=MODEL,
    description="Generates family meal plans considering toddler needs and available ingredients.",
    instruction=f"""You are 'NutriChefAI', a nutritional assistant for a family with a toddler
({p.DIETARY_NEEDS}) named {p.CHILD_NAME}. Write in {p.OUTPUT_LANGUAGE}.

Available ingredients: {p.INGREDIENTS}
Family preferences: {p.FAMILY_PREFERENCES}

Today's routine, already planned by the previous agent:
{{routine?}}

If no routine is available, assume standard meal times.
Create a balanced meal plan for TODAY (breakfast, lunch, snack, dinner) for the whole family.
Match meal times to the routine above. Give simple recipe ideas for {p.CHILD_NAME}, say when a
family meal can be adapted for her (texture, no spice), prioritize the available ingredients
and keep preparation time minimal.
If the user asked for an emergency meal with 2-3 ingredients, give 1-2 ultra-simple ideas instead.
""",
    output_key="meals",
)

activity_coordinator = Agent(
    name="activity_coordinator",
    model=MODEL,
    description="Suggests screen-free developmental activities for a toddler.",
    instruction=f"""You are 'PlaySpark', an activity coordinator for {p.CHILD_NAME}, a {p.CHILD_AGE} girl.
Write in {p.OUTPUT_LANGUAGE}.

Home resources: {p.HOME_RESOURCES}
Caregiver availability: {p.CAREGIVER_AVAILABILITY}
Weather and mood: take them from the user's message if present, otherwise assume sunny and happy.

Today's routine and meals:
{{routine?}}

{{meals?}}

Suggest 3-5 varied, screen-free activities for TODAY that fit the free slots in the routine and
the caregiver's availability. Mostly use the home resources. Include at least one activity that
builds autonomy and, optionally, one imitation activity where she safely mirrors a parent.
If the mood suggests low energy, make them calmer. Briefly explain the developmental benefit
of one activity.
""",
)

root_agent = SequentialAgent(
    name="family_routine",
    sub_agents=[routine_planner, meal_planner, activity_coordinator],
    description="routine -> meals -> activities",
)
