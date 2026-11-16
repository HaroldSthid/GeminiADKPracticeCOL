"""Generic SQLite log store: one row per (subject, date), values kept as JSON."""

import json
import os
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parents[1] / "data" / "handoff.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS handoff_logs (
    subject TEXT NOT NULL,
    date TEXT NOT NULL,
    data TEXT NOT NULL,
    PRIMARY KEY (subject, date)
)
"""


def _today() -> str:
    return date.today().isoformat()


def _connect() -> sqlite3.Connection:
    # Resolved on every call so tests (and users) can point HANDOFF_DB elsewhere.
    path = Path(os.environ.get("HANDOFF_DB", DEFAULT_DB))
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(SCHEMA)
    return conn


def save_entry(subject: str, values: dict[str, str], day: str | None = None, overwrite: bool = True) -> bool:
    """Stores an entry. Returns True if a row was written (False if skipped by overwrite=False)."""
    verb = "INSERT OR REPLACE" if overwrite else "INSERT OR IGNORE"
    with closing(_connect()) as conn, conn:
        cursor = conn.execute(
            f"{verb} INTO handoff_logs (subject, date, data) VALUES (?, ?, ?)",
            (subject, day or _today(), json.dumps(values, ensure_ascii=False)),
        )
    return cursor.rowcount > 0


def recent_entries(limit: int, subject: str | None = None) -> list[dict]:
    """Newest `limit` entries, returned oldest first."""
    query = "SELECT subject, date, data FROM handoff_logs"
    params: list = []
    if subject is not None:
        query += " WHERE subject = ?"
        params.append(subject)
    query += " ORDER BY date DESC, subject DESC LIMIT ?"
    params.append(max(limit, 1))
    with closing(_connect()) as conn:
        rows = conn.execute(query, params).fetchall()
    return [
        {"subject": row["subject"], "date": row["date"], **json.loads(row["data"])}
        for row in reversed(rows)
    ]


MAX_ROWS = 200  # keeps a busy week from flooding the model's context


def entries_for_recent_days(days: int, max_rows: int = MAX_ROWS) -> list[dict]:
    """Every entry of the `days` most recent dates that have entries, oldest first.

    Counts days, not rows: with many subjects per day, `days=2` still returns all of them.
    If that exceeds `max_rows`, the newest `max_rows` entries are kept.
    """
    with closing(_connect()) as conn:
        rows = conn.execute(
            "SELECT subject, date, data FROM handoff_logs "
            "WHERE date IN (SELECT DISTINCT date FROM handoff_logs ORDER BY date DESC LIMIT ?) "
            "ORDER BY date DESC, subject DESC LIMIT ?",
            (max(days, 1), max(max_rows, 1)),
        ).fetchall()
    return [
        {"subject": row["subject"], "date": row["date"], **json.loads(row["data"])}
        for row in reversed(rows)
    ]


def reset_entries() -> int:
    """Deletes every entry. Returns how many rows were removed."""
    with closing(_connect()) as conn, conn:
        return conn.execute("DELETE FROM handoff_logs").rowcount
