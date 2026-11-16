"""The single description a workshop attendee edits to adapt the demo to a company case."""

from dataclasses import dataclass, field

RESERVED_FIELD_NAMES = ("subject", "date")
STAGE_COUNT = 3
FIELD_COUNT = 4


@dataclass(frozen=True)
class Stage:
    """One area of the company that hands work to the next one."""

    key: str  # python identifier: used as agent name and as session-state key
    title: str  # human name, e.g. "Sales"
    receives: str  # what this area receives
    delivers: str  # what this area hands over
    instruction: str  # the area's job rules


@dataclass(frozen=True)
class LogField:
    """One piece of information saved in every log entry."""

    name: str  # lowercase python identifier, unique
    description: str


@dataclass(frozen=True)
class SampleEntry:
    """A fictional log used by the demo seed."""

    days_ago: int
    subject: str
    values: dict[str, str]


@dataclass(frozen=True)
class Domain:
    name: str
    context: dict[str, str]
    coordinator_name: str
    coordinator_role: str
    stages: tuple[Stage, ...]
    log_fields: tuple[LogField, ...]
    subject_label: str
    coach_goal_hint: str
    forbidden_inventions: str
    sample_entries: tuple[SampleEntry, ...] = field(default_factory=tuple)
    output_language: str = "es-LA"

    def _instruction_texts(self) -> dict[str, str]:
        """Every free text that ends up inside an agent instruction."""
        texts = {
            "name": self.name,
            "coordinator_name": self.coordinator_name,
            "coordinator_role": self.coordinator_role,
            "subject_label": self.subject_label,
            "coach_goal_hint": self.coach_goal_hint,
            "forbidden_inventions": self.forbidden_inventions,
        }
        for label, fact in self.context.items():
            texts[f"context[{label!r}]"] = f"{label} {fact}"
        for stage in self.stages:
            for attr in ("title", "receives", "delivers", "instruction"):
                texts[f"stage {stage.key!r} {attr}"] = getattr(stage, attr)
        for log_field in self.log_fields:
            texts[f"log field {log_field.name!r} description"] = log_field.description
        return texts

    def __post_init__(self) -> None:
        # ADK treats {name} in an instruction as a session variable and fails at run time
        # when it does not exist, so literal braces in any text are rejected up front.
        for where, text in self._instruction_texts().items():
            if "{" in text or "}" in text:
                raise ValueError(f"Remove the curly braces from {where}: ADK reads {{text}} as a variable.")
        if len(self.stages) != STAGE_COUNT:
            raise ValueError(f"A domain needs exactly {STAGE_COUNT} stages, got {len(self.stages)}.")
        if len(self.log_fields) != FIELD_COUNT:
            raise ValueError(f"A domain needs exactly {FIELD_COUNT} log fields, got {len(self.log_fields)}.")

        keys = [s.key for s in self.stages]
        for key in keys:
            if not key.isidentifier():
                raise ValueError(f"Stage key {key!r} must be a python identifier (letters, digits, underscore).")
        if len(set(keys)) != len(keys):
            raise ValueError(f"Stage keys must be unique, got {keys}.")

        names = [f.name for f in self.log_fields]
        for name in names:
            if not (name.isidentifier() and name == name.lower()):
                raise ValueError(f"Log field {name!r} must be a lowercase python identifier.")
            if name in RESERVED_FIELD_NAMES:
                raise ValueError(f"Log field {name!r} is reserved; do not use {RESERVED_FIELD_NAMES}.")
        if len(set(names)) != len(names):
            raise ValueError(f"Log field names must be unique, got {names}.")
        if set(names) & set(keys):
            raise ValueError("A log field name cannot equal a stage key.")

        seen_days: set[int] = set()
        for entry in self.sample_entries:
            if entry.days_ago < 1:
                raise ValueError(f"Sample entry days_ago must be >= 1, got {entry.days_ago}.")
            if entry.days_ago in seen_days:
                raise ValueError(f"Sample entry days_ago must be unique, {entry.days_ago} is repeated.")
            seen_days.add(entry.days_ago)
            unknown = set(entry.values) - set(names)
            if unknown:
                raise ValueError(f"Sample entry {entry.subject!r} uses undeclared fields: {sorted(unknown)}.")
