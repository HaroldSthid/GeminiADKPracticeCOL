import pytest

from handoff_kit import store

FIELDS = {"f1": "a", "f2": "b", "f3": "c", "f4": "d"}


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("HANDOFF_DB", str(tmp_path / "x.db"))


def test_round_trip():
    store.save_entry("O-1", FIELDS, day="2026-01-01")
    rows = store.recent_entries(5)
    assert rows == [{"subject": "O-1", "date": "2026-01-01", **FIELDS}]


def test_same_subject_and_date_replaces():
    store.save_entry("O-1", FIELDS, day="2026-01-01")
    store.save_entry("O-1", {**FIELDS, "f1": "new"}, day="2026-01-01")
    rows = store.recent_entries(5)
    assert len(rows) == 1 and rows[0]["f1"] == "new"


def test_defaults_to_today(monkeypatch):
    monkeypatch.setattr(store, "_today", lambda: "2026-02-02")
    store.save_entry("O-1", FIELDS)
    assert store.recent_entries(1)[0]["date"] == "2026-02-02"


def test_oldest_first_and_limited():
    for day in ("2026-01-01", "2026-01-02", "2026-01-03"):
        store.save_entry("O-1", FIELDS, day=day)
    assert [r["date"] for r in store.recent_entries(2)] == ["2026-01-02", "2026-01-03"]


def test_filter_by_subject():
    store.save_entry("O-1", FIELDS, day="2026-01-01")
    store.save_entry("O-2", FIELDS, day="2026-01-02")
    assert [r["subject"] for r in store.recent_entries(5, subject="O-2")] == ["O-2"]


def test_insert_only_does_not_overwrite():
    store.save_entry("O-1", FIELDS, day="2026-01-01")
    assert store.save_entry("O-1", {**FIELDS, "f1": "x"}, day="2026-01-01", overwrite=False) is False
    assert store.recent_entries(1)[0]["f1"] == "a"


def test_recent_days_returns_every_entry_of_the_latest_days_not_a_row_count():
    for day in ("2026-01-01", "2026-01-02", "2026-01-03"):
        for subject in ("O-1", "O-2", "O-3"):
            store.save_entry(subject, FIELDS, day=day)

    rows = store.entries_for_recent_days(2)

    assert len(rows) == 6
    assert {r["date"] for r in rows} == {"2026-01-02", "2026-01-03"}
    assert [r["date"] for r in rows] == sorted(r["date"] for r in rows)


def test_recent_days_counts_only_days_that_have_entries():
    store.save_entry("O-1", FIELDS, day="2026-01-01")
    store.save_entry("O-1", FIELDS, day="2026-01-10")

    rows = store.entries_for_recent_days(2)

    assert [r["date"] for r in rows] == ["2026-01-01", "2026-01-10"]


def test_recent_days_caps_rows_keeping_the_newest():
    for n in range(5):
        store.save_entry(f"O-{n}", FIELDS, day="2026-01-01")
    store.save_entry("O-new", FIELDS, day="2026-01-02")

    rows = store.entries_for_recent_days(2, max_rows=3)

    assert len(rows) == 3
    assert rows[-1]["subject"] == "O-new"


def test_recent_days_on_empty_store():
    assert store.entries_for_recent_days(7) == []


def test_reset_returns_deleted_count():
    store.save_entry("O-1", FIELDS, day="2026-01-01")
    store.save_entry("O-2", FIELDS, day="2026-01-01")
    assert store.reset_entries() == 2
    assert store.recent_entries(5) == []
