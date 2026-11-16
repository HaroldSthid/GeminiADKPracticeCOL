import inspect

import pytest
from google.adk.tools.function_tool import FunctionTool

from handoff_kit import store
from handoff_kit.domains import load_domain
from handoff_kit.tools import build_tools

DOMAIN = load_domain("company_orders")


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("HANDOFF_DB", str(tmp_path / "x.db"))


def test_adk_declaration_lists_domain_field_names():
    save_log, _ = build_tools(DOMAIN)
    decl = FunctionTool(save_log)._get_declaration()
    # This ADK version exposes the schema as parameters_json_schema (parameters is None).
    schema = decl.parameters_json_schema
    expected = ["subject", *(f.name for f in DOMAIN.log_fields)]
    assert list(schema["properties"]) == expected
    assert schema["required"] == expected
    assert decl.name == "save_log"


def test_docstring_comes_from_the_domain():
    save_log, _ = build_tools(DOMAIN)
    assert DOMAIN.subject_label in save_log.__doc__
    for field in DOMAIN.log_fields:
        assert field.description in save_log.__doc__
    assert "unknown" in save_log.__doc__


def test_signature_has_named_str_parameters():
    save_log, _ = build_tools(DOMAIN)
    names = list(inspect.signature(save_log).parameters)
    assert names == ["subject", *(f.name for f in DOMAIN.log_fields)]


def test_save_log_persists_exactly_the_named_values(monkeypatch):
    monkeypatch.setattr(store, "_today", lambda: "2026-03-03")
    save_log, _ = build_tools(DOMAIN)
    values = {f.name: f"v-{f.name}" for f in DOMAIN.log_fields}
    result = save_log(subject="PED-1", **values)
    assert result["status"] == "saved"
    assert store.recent_entries(1) == [{"subject": "PED-1", "date": "2026-03-03", **values}]


def test_get_recent_logs_counts_days_so_many_orders_in_one_day_are_all_returned():
    save_log, get_recent_logs = build_tools(DOMAIN)
    values = {f.name: "x" for f in DOMAIN.log_fields}
    for order in ("1", "2", "3"):
        store.save_entry(order, values, day="2026-03-03")

    result = get_recent_logs(1)

    assert [log["subject"] for log in result["logs"]] == ["1", "2", "3"]


def test_get_recent_logs_empty_then_ok():
    save_log, get_recent_logs = build_tools(DOMAIN)
    assert get_recent_logs(7)["status"] == "empty"
    save_log(subject="PED-1", **{f.name: "x" for f in DOMAIN.log_fields})
    result = get_recent_logs(7)
    assert result["status"] == "ok" and result["logs"][0]["subject"] == "PED-1"
