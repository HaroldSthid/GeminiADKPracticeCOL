import importlib
import os
import pkgutil

from ..domain import Domain

DEFAULT_DOMAIN = "company_orders"


def available_domains() -> list[str]:
    return sorted(m.name for m in pkgutil.iter_modules(__path__) if not m.name.startswith("_"))


def load_domain(name: str | None = None) -> Domain:
    """Loads DOMAIN from handoff_kit/domains/<name>.py (arg, else HANDOFF_DOMAIN, else company_orders)."""
    name = name or os.environ.get("HANDOFF_DOMAIN") or DEFAULT_DOMAIN
    if name not in available_domains() and name != "_template":
        raise ValueError(f"Unknown domain {name!r}. Available domains: {', '.join(available_domains())}.")
    return importlib.import_module(f"{__name__}.{name}").DOMAIN
