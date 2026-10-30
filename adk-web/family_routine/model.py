import asyncio

import httpx
from google.adk.models.google_llm import Gemini

ATTEMPTS = 3
BASE_DELAY = 2.0  # seconds; doubles after each failed attempt


class RetryingGemini(Gemini):
    """Gemini that retries when the connection drops before any response arrives.

    The built-in retry_options cover timeouts, connect errors and 429/5xx, but not
    httpx.ReadError, which is what an unstable network raises mid-request.
    """

    async def generate_content_async(self, llm_request, stream=False):
        for attempt in range(1, ATTEMPTS + 1):
            yielded = False
            try:
                async for response in super().generate_content_async(llm_request, stream):
                    yielded = True
                    yield response
                return
            except httpx.TransportError:
                # After a partial response a retry would duplicate output, so fail instead.
                if yielded or attempt == ATTEMPTS:
                    raise
                await asyncio.sleep(BASE_DELAY * 2 ** (attempt - 1))


def flash() -> RetryingGemini:
    return RetryingGemini(model="gemini-flash-latest")
