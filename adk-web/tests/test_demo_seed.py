from datetime import date

import pytest

from family_routine.demo_seed import reset_logs, seed_demo_logs
from family_routine.tools import get_recent_logs, save_day_log


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv("FAMILY_DB", str(tmp_path / "family.db"))


TODAY = date(2026, 11, 20)


def test_seed_inserts_five_consecutive_days_ending_yesterday():
    inserted = seed_demo_logs(today=TODAY)

    logs = get_recent_logs(10)["logs"]
    assert inserted == 5
    assert [log["date"] for log in logs] == [
        "2026-11-15",
        "2026-11-16",
        "2026-11-17",
        "2026-11-18",
        "2026-11-19",
    ]


def test_seed_never_creates_a_log_for_today():
    seed_demo_logs(today=TODAY)

    dates = [log["date"] for log in get_recent_logs(10)["logs"]]
    assert TODAY.isoformat() not in dates


def test_seed_does_not_overwrite_existing_logs(monkeypatch):
    monkeypatch.setattr("family_routine.tools._today", lambda: "2026-11-19")
    save_day_log("5:00", "ninguna", "real", "dato real del usuario")

    inserted = seed_demo_logs(today=TODAY)

    logs = {log["date"]: log for log in get_recent_logs(10)["logs"]}
    assert inserted == 4
    assert logs["2026-11-19"]["notes"] == "dato real del usuario"


def test_seed_is_idempotent():
    seed_demo_logs(today=TODAY)

    assert seed_demo_logs(today=TODAY) == 0
    assert len(get_recent_logs(10)["logs"]) == 5


def test_reset_removes_every_log_and_reports_how_many():
    seed_demo_logs(today=TODAY)

    assert reset_logs() == 5
    assert get_recent_logs(10)["status"] == "empty"


def test_reset_on_empty_database_returns_zero():
    assert reset_logs() == 0
