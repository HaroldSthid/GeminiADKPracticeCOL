import asyncio

import httpx
import pytest
from google.adk.models.google_llm import Gemini

from family_routine import model as model_module
from family_routine.model import RetryingGemini


@pytest.fixture(autouse=True)
def no_sleep(monkeypatch):
    monkeypatch.setattr(model_module, "BASE_DELAY", 0)


def collect(llm):
    async def run():
        return [r async for r in llm.generate_content_async(llm_request=None)]

    return asyncio.run(run())


def flaky_parent(failures, error=httpx.ReadError("boom")):
    calls = {"n": 0}

    async def fake(self, llm_request, stream=False):
        calls["n"] += 1
        if calls["n"] <= failures:
            raise error
        yield "ok"

    return fake, calls


def test_retries_a_read_error_and_then_succeeds(monkeypatch):
    fake, calls = flaky_parent(failures=2)
    monkeypatch.setattr(Gemini, "generate_content_async", fake)
    assert collect(RetryingGemini(model="m")) == ["ok"]
    assert calls["n"] == 3


def test_gives_up_after_the_last_attempt(monkeypatch):
    fake, calls = flaky_parent(failures=99)
    monkeypatch.setattr(Gemini, "generate_content_async", fake)
    with pytest.raises(httpx.ReadError):
        collect(RetryingGemini(model="m"))
    assert calls["n"] == model_module.ATTEMPTS


def test_does_not_retry_other_errors(monkeypatch):
    fake, calls = flaky_parent(failures=99, error=ValueError("bad request"))
    monkeypatch.setattr(Gemini, "generate_content_async", fake)
    with pytest.raises(ValueError):
        collect(RetryingGemini(model="m"))
    assert calls["n"] == 1


def test_does_not_retry_after_a_partial_response(monkeypatch):
    calls = {"n": 0}

    async def fake(self, llm_request, stream=False):
        calls["n"] += 1
        yield "partial"
        raise httpx.ReadError("cut mid-stream")

    monkeypatch.setattr(Gemini, "generate_content_async", fake)
    with pytest.raises(httpx.ReadError):
        collect(RetryingGemini(model="m"))
    assert calls["n"] == 1
