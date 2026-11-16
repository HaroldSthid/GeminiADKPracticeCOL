from dataclasses import replace

import pytest

from handoff_kit.domain import Domain, LogField, SampleEntry, Stage


def make_stage(key, title="T"):
    return Stage(key=key, title=title, receives="r", delivers="d", instruction="i")


def make_domain(**overrides):
    base = dict(
        name="Test",
        context={"Company": "Acme"},
        coordinator_name="Dispatcher",
        coordinator_role="Routes work.",
        stages=(make_stage("a"), make_stage("b"), make_stage("c")),
        log_fields=(
            LogField("f1", "first"),
            LogField("f2", "second"),
            LogField("f3", "third"),
            LogField("f4", "fourth"),
        ),
        subject_label="case",
        coach_goal_hint="look for delays",
        forbidden_inventions="Never invent dates.",
        sample_entries=(SampleEntry(1, "X-1", {"f1": "v"}),),
    )
    base.update(overrides)
    return Domain(**base)


def _stage_with_instruction(text):
    return (
        Stage(key="a", title="T", receives="r", delivers="d", instruction=text),
        make_stage("b"),
        make_stage("c"),
    )


@pytest.mark.parametrize(
    "overrides",
    [
        {"context": {"Company": "Uses {customer_id} here"}},
        {"stages": _stage_with_instruction("Reply as {json}")},
        {"forbidden_inventions": "Never invent {dates}."},
        {"coach_goal_hint": "look for {delays}"},
        {"coordinator_role": "Routes {work}."},
        {
            "log_fields": (
                LogField("f1", "the {first}"),
                LogField("f2", "second"),
                LogField("f3", "third"),
                LogField("f4", "fourth"),
            )
        },
    ],
)
def test_curly_braces_in_text_are_rejected_because_adk_treats_them_as_variables(overrides):
    with pytest.raises(ValueError, match="curly braces"):
        make_domain(**overrides)


def test_valid_domain_builds_with_default_language():
    assert make_domain().output_language == "es-LA"


def test_needs_exactly_three_stages():
    with pytest.raises(ValueError, match="3 stages"):
        make_domain(stages=(make_stage("a"), make_stage("b")))


def test_needs_exactly_four_log_fields():
    with pytest.raises(ValueError, match="4 log fields"):
        make_domain(log_fields=(LogField("f1", "x"),))


def test_stage_key_must_be_identifier():
    with pytest.raises(ValueError, match="identifier"):
        make_domain(stages=(make_stage("a b"), make_stage("b"), make_stage("c")))


def test_stage_keys_must_be_unique():
    with pytest.raises(ValueError, match="unique"):
        make_domain(stages=(make_stage("a"), make_stage("a"), make_stage("c")))


def test_field_name_must_be_lowercase_identifier():
    fields = (LogField("Bad", "x"), LogField("f2", "x"), LogField("f3", "x"), LogField("f4", "x"))
    with pytest.raises(ValueError, match="lowercase"):
        make_domain(log_fields=fields)


def test_field_names_must_be_unique():
    fields = (LogField("f1", "x"), LogField("f1", "x"), LogField("f3", "x"), LogField("f4", "x"))
    with pytest.raises(ValueError, match="unique"):
        make_domain(log_fields=fields)


@pytest.mark.parametrize("reserved", ["subject", "date"])
def test_field_cannot_collide_with_reserved_names(reserved):
    fields = (LogField(reserved, "x"), LogField("f2", "x"), LogField("f3", "x"), LogField("f4", "x"))
    with pytest.raises(ValueError, match="reserved"):
        make_domain(log_fields=fields)


def test_sample_entry_cannot_use_undeclared_field():
    with pytest.raises(ValueError, match="undeclared"):
        make_domain(sample_entries=(SampleEntry(1, "X", {"nope": "v"}),))


def test_sample_entry_days_ago_must_be_unique():
    entries = (SampleEntry(1, "X", {"f1": "v"}), SampleEntry(1, "Y", {"f1": "v"}))
    with pytest.raises(ValueError, match="days_ago"):
        make_domain(sample_entries=entries)


def test_sample_entry_days_ago_must_be_at_least_one():
    with pytest.raises(ValueError, match="days_ago"):
        make_domain(sample_entries=(SampleEntry(0, "X", {"f1": "v"}),))


def test_domain_is_frozen():
    with pytest.raises(Exception):
        replace(make_domain()).name = "other"
