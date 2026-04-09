"""NVEIL API client — handles HTTP communication with the NVEIL server."""

import logging
import httpx

from .exceptions import (
    AuthenticationError,
    QuotaExceededError,
    ScopeError,
    SpecGenerationError,
)

DEFAULT_BASE_URL = "https://app.nveil.com"
DEFAULT_TIMEOUT = 120.0


class NveilClient:
    """HTTP client for the NVEIL public API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        verify: bool = True,
    ):
        from . import __version__

        if not verify:
            logging.getLogger("nveil").warning(
                "SSL verification disabled (verify=False). "
                "Only use this for local development with self-signed certificates."
            )
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={
                "X-API-Key": api_key,
                "X-Nveil-Schema-Version": __version__,
            },
            timeout=timeout,
            verify=verify,
        )

    def _handle_response(self, resp: httpx.Response) -> dict:
        if resp.status_code == 401:
            raise AuthenticationError(
                "Invalid, expired, or revoked API key"
            )
        if resp.status_code == 403:
            raise ScopeError(resp.json().get("detail", "Missing required scope"))
        if resp.status_code == 429:
            raise QuotaExceededError("Rate limit exceeded")
        if resp.status_code >= 400:
            detail = resp.text
            try:
                detail = resp.json().get("detail", resp.text)
            except Exception:
                pass
            raise SpecGenerationError(f"API error ({resp.status_code}): {detail}")
        return resp.json()

    def processing_plan(
        self,
        prompt: str,
        request_blob: str,
        catalogue_stats: str,
    ) -> dict:
        """Request a data processing plan from the server.

        Args:
            prompt: User's natural language prompt.
            request_blob: Base64-encoded encrypted request payload.
            catalogue_stats: JSON string of dataset metadata.
        """
        resp = self._client.post(
            "/api/v1/processing/plan",
            json={
                "prompt": prompt,
                "request_blob": request_blob,
                "catalogue_stats": catalogue_stats,
            },
        )
        return self._handle_response(resp)

    def visualization_generate(
        self,
        session_id: str,
        request_blob: str,
    ) -> dict:
        """Request visualization generation from the server.

        Args:
            session_id: Session ID from processing_plan response.
            request_blob: Base64-encoded encrypted request payload.
        """
        resp = self._client.post(
            "/api/v1/visualization/generate",
            json={
                "session_id": session_id,
                "request_blob": request_blob,
            },
        )
        return self._handle_response(resp)

    def close(self):
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
