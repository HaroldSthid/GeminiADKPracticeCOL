import importlib

import pytest

from handoff_kit.domain import Domain
from handoff_kit.domains import load_domain


def test_default_is_company_orders(monkeypatch):
    monkeypatch.delenv("HANDOFF_DOMAIN", raising=False)
    assert load_domain() is importlib.import_module("handoff_kit.domains.company_orders").DOMAIN


def test_env_selects_domain(monkeypatch):
    monkeypatch.setenv("HANDOFF_DOMAIN", "_template")
    assert load_domain().name.startswith("TODO")


def test_unknown_name_lists_available_domains():
    with pytest.raises(ValueError) as err:
        load_domain("nope")
    assert "company_orders" in str(err.value)
    assert "_template" not in str(err.value)


def test_template_imports_and_validates():
    assert isinstance(load_domain("_template"), Domain)


def test_company_orders_sample_subjects_match_how_users_type_them():
    # Users say "pedido 2087", so the log is keyed by "2087": no invented prefix in the seed.
    domain = load_domain("company_orders")
    for entry in domain.sample_entries:
        assert entry.subject.isdigit()
        assert entry.subject in entry.values["order_and_customer"]


def test_company_orders_shape():
    domain = load_domain("company_orders")
    assert len(domain.stages) == 3
    assert len(domain.log_fields) == 4
    assert len(domain.sample_entries) == 5
    assert [f.name for f in domain.log_fields] == [
        "order_and_customer",
        "requested_change",
        "received_by_and_when",
        "status",
    ]
