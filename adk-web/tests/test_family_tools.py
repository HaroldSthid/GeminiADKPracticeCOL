import pytest

from family_routine import tools
from family_routine.tools import get_recent_logs, save_day_log


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("FAMILY_DB", str(tmp_path / "family.db"))


def test_get_recent_logs_empty():
    assert get_recent_logs(7)["status"] == "empty"


def test_save_then_read_returns_the_entry():
    save_day_log("6:40 AM", "short", "happy", "tried broccoli")
    result = get_recent_logs(1)
    assert result["status"] == "ok"
    assert result["logs"][0]["wake_up_time"] == "6:40 AM"


def test_saving_twice_on_the_same_day_replaces_the_entry():
    save_day_log("6:40 AM", "short", "happy", "")
    save_day_log("6:45 AM", "long", "tired", "")
    logs = get_recent_logs(7)["logs"]
    assert len(logs) == 1
    assert logs[0]["mood"] == "tired"


def test_logs_come_back_oldest_first_and_limited(monkeypatch):
    for day in ("2026-01-01", "2026-01-02", "2026-01-03"):
        monkeypatch.setattr(tools, "_today", lambda day=day: day)
        save_day_log(f"wake {day}", "ok", "ok", "")
    logs = get_recent_logs(2)["logs"]
    assert [log["date"] for log in logs] == ["2026-01-02", "2026-01-03"]


def test_data_survives_a_new_connection(tmp_path, monkeypatch):
    save_day_log("6:40 AM", "short", "happy", "")
    monkeypatch.setenv("FAMILY_DB", str(tmp_path / "family.db"))  # same file, fresh connection
    assert get_recent_logs(1)["status"] == "ok"
