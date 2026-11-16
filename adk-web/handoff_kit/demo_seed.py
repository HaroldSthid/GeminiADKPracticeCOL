"""Demo data for the workshop: five fictional days of logs for the weekly coach.

Usage (from adk-web/):
    python -m handoff_kit.demo_seed                  # add the sample entries
    python -m handoff_kit.demo_seed --reset          # delete every log
    python -m handoff_kit.demo_seed --domain NAME    # use another domain module

Existing logs are never overwritten and nothing is written for today, so the
"save today's log" step of the demo still works.
"""

import argparse
import os
from datetime import date, timedelta

from . import store
from .domain import Domain
from .domains import load_domain


def seed_demo_logs(domain: Domain, today: date | None = None) -> int:
    """Inserts the domain's sample entries at today - days_ago. Returns how many rows were added."""
    today = today or date.today()
    inserted = 0
    for entry in domain.sample_entries:
        day = (today - timedelta(days=entry.days_ago)).isoformat()
        if store.save_entry(entry.subject, entry.values, day=day, overwrite=False):
            inserted += 1
    return inserted


def reset_logs() -> int:
    """Deletes every log. Returns how many rows were removed."""
    return store.reset_entries()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Seed or reset the demo diary of one domain.")
    parser.add_argument("--reset", action="store_true", help="delete all logs instead of seeding")
    parser.add_argument("--domain", default=None, help="domain module name (default: HANDOFF_DOMAIN or company_orders)")
    args = parser.parse_args(argv)
    if args.domain:
        # The diary file is chosen from HANDOFF_DOMAIN, so --domain also selects that domain's diary.
        os.environ["HANDOFF_DOMAIN"] = args.domain
    if args.reset:
        print(f"Deleted {reset_logs()} log(s). The diary is empty.")
    else:
        print(f"Added {seed_demo_logs(load_domain(args.domain))} demo log(s).")


if __name__ == "__main__":
    main()
