"""TEMPLATE: copy this file to handoff_kit/domains/<your_case>.py and edit ONLY this file.

Then run it with:   HANDOFF_DOMAIN=<your_case>   (PowerShell: $env:HANDOFF_DOMAIN = "<your_case>")
Every comment below explains, in plain words, what to write. Replace each TODO.
Keep the structure: exactly 3 stages and exactly 4 log fields.
"""

from ..domain import Domain, LogField, SampleEntry, Stage

DOMAIN = Domain(
    # A short name for your case, shown to the agents. Example: "Order address changes".
    name="TODO: name of your case",
    # Language the agents answer in. "es-LA" = Latin American Spanish.
    output_language="es-LA",
    # Facts the agents must know about your company. Each entry is a label and a sentence.
    # Include: what the company does, working hours, rules, deadlines, and the problem you
    # want to solve. Agents will treat these as true, so only write real facts.
    context={
        "Company": "TODO: one sentence about the company",
        "Rules": "TODO: the business rules or deadlines that matter",
        "Problem": "TODO: where information gets lost between areas",
    },
    # The dispatcher: the agent that talks to the user and calls the areas.
    # Name it anything you like.
    coordinator_name="TODO: dispatcher name",
    # One paragraph: what the dispatcher coordinates and why.
    coordinator_role="TODO: one paragraph describing what the dispatcher coordinates",
    # The three areas that hand work to each other, IN ORDER. Each area reads the output
    # of the previous ones automatically.
    stages=(
        Stage(
            # Short id with letters, digits and underscores only (no spaces). Example: "sales".
            key="stage_one",
            # Human name of the area. Example: "Sales".
            title="TODO: first area",
            # What this area gets as input (from the customer or user).
            receives="TODO: what the first area receives",
            # What this area hands to the next one.
            delivers="TODO: what the first area hands over",
            # The rules of its job: what it must check, write and flag.
            instruction="TODO: the job rules of the first area",
        ),
        Stage(
            key="stage_two",
            title="TODO: second area",
            receives="TODO: what the second area receives (the first area's output)",
            delivers="TODO: what the second area hands over",
            instruction="TODO: the job rules of the second area",
        ),
        Stage(
            key="stage_three",
            title="TODO: third area",
            receives="TODO: what the third area receives (the second area's output)",
            delivers="TODO: the final result for the user or customer",
            instruction="TODO: the job rules of the third area",
        ),
    ),
    # The four facts saved in every daily log. These become the form the agent fills in.
    # name: lowercase letters and underscores; do not use "subject" or "date".
    # description: what to write there, with a short example.
    log_fields=(
        LogField("field_one", "TODO: what goes in field one, e.g. an example"),
        LogField("field_two", "TODO: what goes in field two"),
        LogField("field_three", "TODO: what goes in field three"),
        LogField("field_four", "TODO: what goes in field four"),
    ),
    # What each log is about. Example: "order", "case", "ticket".
    subject_label="TODO: order or case or ticket",
    # What the weekly coach should look for across the logs. Example: "delays and what
    # they have in common".
    coach_goal_hint="TODO: what the weekly coach looks for",
    # The most important rule of the workshop: what the agents must NEVER make up.
    forbidden_inventions="TODO: e.g. Never invent dates. Never confirm what the log does not record.",
    # Five fictional logs for the demo, one per day. days_ago is 1..5 (yesterday = 1).
    # Hide a pattern in them (for example, late cases share the same cause) so the coach
    # can discover it. Use only the four field names above.
    sample_entries=(
        SampleEntry(5, "TODO-1", {"field_one": "TODO", "field_two": "TODO", "field_three": "TODO", "field_four": "TODO"}),
        SampleEntry(4, "TODO-2", {"field_one": "TODO", "field_two": "TODO", "field_three": "TODO", "field_four": "TODO"}),
        SampleEntry(3, "TODO-3", {"field_one": "TODO", "field_two": "TODO", "field_three": "TODO", "field_four": "TODO"}),
        SampleEntry(2, "TODO-4", {"field_one": "TODO", "field_two": "TODO", "field_three": "TODO", "field_four": "TODO"}),
        SampleEntry(1, "TODO-5", {"field_one": "TODO", "field_two": "TODO", "field_three": "TODO", "field_four": "TODO"}),
    ),
)
