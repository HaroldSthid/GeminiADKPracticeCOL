"""Demo data for the workshop: five fictional days of logs for the weekly coach.

Usage (from adk-web/):
    python -m family_routine.demo_seed          # add the five days
    python -m family_routine.demo_seed --reset  # delete every log, back to an empty diary

The data holds one pattern the coach can discover: naps are long on days with a
morning outing and a bedtime story ritual in a dark room, and short on days without them.
Existing logs are never overwritten, and no log is created for today, so the
"save today's log" step of the demo still works.
"""

import argparse
from contextlib import closing
from datetime import date, timedelta

from . import profile as p
from .tools import _connect

# Oldest first. Text is Spanish because the demo audience reads it in the chat.
DEMO_DAYS = [
    ("6:30", "2 horas", "tranquila", "Paseo en la mañana. Siesta en cuarto oscuro con cuento."),
    ("6:50", "45 minutos", "irritable por la tarde", "Sin salida al parque. Siesta con luz y ruido de la calle."),
    ("6:40", "1 hora 50 minutos", "feliz", "Salida al parque en la mañana. Ritual de cuento antes de la siesta."),
    ("7:10", "40 minutos", "cansada", "Se durmió en el carro y la siesta fue corta. Sin ritual."),
    ("6:35", "1 hora 45 minutos", "buen humor", "Paseo en la mañana. Cuento y cuarto en penumbra."),
]


def seed_demo_logs(today: date | None = None) -> int:
    """Inserts the demo days ending yesterday. Returns how many rows were added."""
    today = today or date.today()
    start = today - timedelta(days=len(DEMO_DAYS))
    inserted = 0
    with closing(_connect()) as conn, conn:
        for offset, (wake_up, nap, mood, notes) in enumerate(DEMO_DAYS):
            day = (start + timedelta(days=offset)).isoformat()
            cursor = conn.execute(
                "INSERT OR IGNORE INTO day_logs (child, date, wake_up_time, nap, mood, notes) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (p.CHILD_NAME, day, wake_up, nap, mood, notes),
            )
            inserted += cursor.rowcount
    return inserted


def reset_logs() -> int:
    """Deletes every log of the configured child. Returns how many rows were removed."""
    with closing(_connect()) as conn, conn:
        return conn.execute("DELETE FROM day_logs WHERE child = ?", (p.CHILD_NAME,)).rowcount


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed or reset the demo diary.")
    parser.add_argument("--reset", action="store_true", help="delete all logs instead of seeding")
    args = parser.parse_args()
    if args.reset:
        print(f"Deleted {reset_logs()} log(s). The diary is empty.")
    else:
        print(f"Added {seed_demo_logs()} demo log(s).")


if __name__ == "__main__":
    main()
