"""Tool factory: builds the LLM-callable functions from a Domain."""

import inspect
from collections.abc import Callable

from . import store
from .domain import Domain


def build_tools(domain: Domain) -> tuple[Callable, Callable]:
    """Returns (save_log, get_recent_logs). save_log has one named str parameter per log field."""
    names = [f.name for f in domain.log_fields]

    def save_log(subject: str, **values: str) -> dict:
        entry = {name: values.get(name, "unknown") for name in names}
        store.save_entry(subject, entry)
        return {"status": "saved", "entry": {"subject": subject, "date": store._today(), **entry}}

    # ADK builds the function declaration from signature, annotations and docstring,
    # so we expose the domain's field names as real named parameters.
    params = [inspect.Parameter("subject", inspect.Parameter.KEYWORD_ONLY, annotation=str)]
    params += [inspect.Parameter(n, inspect.Parameter.KEYWORD_ONLY, annotation=str) for n in names]

    arg_lines = [f"        subject: The {domain.subject_label} this log is about (its identifier)."]
    arg_lines += [f"        {f.name}: {f.description}" for f in domain.log_fields]
    doc = (
        f"Saves today's log for one {domain.subject_label} so later days and the weekly review can use it.\n\n"
        "    Use 'unknown' for anything the user did not say; never invent it.\n\n"
        "    Args:\n" + "\n".join(arg_lines) + "\n    "
    )

    save_log.__name__ = "save_log"
    save_log.__doc__ = doc
    save_log.__signature__ = inspect.Signature(params, return_annotation=dict)
    save_log.__annotations__ = {**{p.name: str for p in params}, "return": dict}

    def get_recent_logs(days: int) -> dict:
        """Returns every saved log of the most recent days, oldest first.

        Args:
            days: How many of the latest days to read (2 for the last days, 7 for a week).
        """
        rows = store.entries_for_recent_days(days)
        if not rows:
            return {"status": "empty", "message": "No logs saved yet."}
        return {"status": "ok", "logs": rows}

    return save_log, get_recent_logs
