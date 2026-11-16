from datetime import date, timedelta

import pytest

from handoff_kit import store
from handoff_kit.demo_seed import reset_logs, seed_demo_logs
from handoff_kit.domains import load_domain

DOMAIN = load_domain("company_orders")
TODAY = date(2026, 11, 20)


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv("HANDOFF_DB", str(tmp_path / "x.db"))


def test_seed_inserts_five_consecutive_days_ending_yesterday():
    assert seed_demo_logs(DOMAIN, today=TODAY) == 5
    dates = [r["date"] for r in store.recent_entries(10)]
    assert dates == ["2026-11-15", "2026-11-16", "2026-11-17", "2026-11-18", "2026-11-19"]


def test_seed_never_writes_today():
    seed_demo_logs(DOMAIN, today=TODAY)
    assert TODAY.isoformat() not in [r["date"] for r in store.recent_entries(10)]


def test_seed_is_idempotent():
    seed_demo_logs(DOMAIN, today=TODAY)
    assert seed_demo_logs(DOMAIN, today=TODAY) == 0
    assert len(store.recent_entries(10)) == 5


def test_seed_does_not_overwrite_existing():
    entry = DOMAIN.sample_entries[0]
    day = (TODAY - timedelta(days=entry.days_ago)).isoformat()
    real = {f.name: "real" for f in DOMAIN.log_fields}
    store.save_entry(entry.subject, real, day=day)
    assert seed_demo_logs(DOMAIN, today=TODAY) == 4
    row = [r for r in store.recent_entries(10) if r["date"] == day][0]
    assert row["status"] == "real"


def test_reset_reports_count():
    seed_demo_logs(DOMAIN, today=TODAY)
    assert reset_logs() == 5
    assert store.recent_entries(10) == []
    assert reset_logs() == 0
