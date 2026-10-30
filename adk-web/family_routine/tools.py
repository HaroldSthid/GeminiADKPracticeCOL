import os
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

from . import profile as p

DEFAULT_DB = Path(__file__).resolve().parents[1] / "data" / "family.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS day_logs (
    child TEXT NOT NULL,
    date TEXT NOT NULL,
    wake_up_time TEXT,
    nap TEXT,
    mood TEXT,
    notes TEXT,
    PRIMARY KEY (child, date)
)
"""


def _today() -> str:
    return date.today().isoformat()


def _connect() -> sqlite3.Connection:
    # Resolved on every call so tests (and users) can point FAMILY_DB elsewhere.
    path = Path(os.environ.get("FAMILY_DB", DEFAULT_DB))
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def save_day_log(wake_up_time: str, nap: str, mood: str, notes: str) -> dict:
    """Saves today's log so tomorrow's routine and the weekly review can use it.

    Args:
        wake_up_time: Time the child woke up today, e.g. "6:40 AM".
        nap: How the nap went, e.g. "short, 40 minutes".
        mood: The child's overall mood today.
        notes: Anything else worth remembering (food, tantrums, new skills).
    """
    entry = {
        "date": _today(),
        "wake_up_time": wake_up_time,
        "nap": nap,
        "mood": mood,
        "notes": notes,
    }
    with closing(_connect()) as conn, conn:
        conn.execute(
            "INSERT OR REPLACE INTO day_logs (child, date, wake_up_time, nap, mood, notes) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (p.CHILD_NAME, *entry.values()),
        )
    return {"status": "saved", "entry": entry}


def get_recent_logs(days: int) -> dict:
    """Returns the most recent saved day logs, oldest first.

    Args:
        days: How many of the latest logs to return (1 for yesterday's, 7 for a week).
    """
    with closing(_connect()) as conn:
        rows = conn.execute(
            "SELECT date, wake_up_time, nap, mood, notes FROM day_logs "
            "WHERE child = ? ORDER BY date DESC LIMIT ?",
            (p.CHILD_NAME, max(days, 1)),
        ).fetchall()
    if not rows:
        return {"status": "empty", "message": "No logs saved yet."}
    return {"status": "ok", "logs": [dict(row) for row in reversed(rows)]}
