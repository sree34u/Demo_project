"""Reusable requests-based HTTP client returning typed ApiResponse objects."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from config.settings import get_settings
from models.api_response import ApiResponse
from utils.logger import get_logger

_logger = get_logger(__name__)


class BaseApiClient:
    """Thin wrapper around requests.Session for consistent API interactions."""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None) -> None:
        settings = get_settings()
        self._base_url = (base_url or settings.api_base_url).rstrip("/")
        self._timeout = timeout or settings.api_timeout_seconds
        self._session = requests.Session()

    def close(self) -> None:
        self._session.close()

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> ApiResponse:
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json_body: Optional[Dict[str, Any]] = None, **kwargs: Any) -> ApiResponse:
        return self._request("POST", endpoint, json=json_body, **kwargs)

    def put(self, endpoint: str, json_body: Optional[Dict[str, Any]] = None, **kwargs: Any) -> ApiResponse:
        return self._request("PUT", endpoint, json=json_body, **kwargs)

    def patch(self, endpoint: str, json_body: Optional[Dict[str, Any]] = None, **kwargs: Any) -> ApiResponse:
        return self._request("PATCH", endpoint, json=json_body, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> ApiResponse:
        return self._request("DELETE", endpoint, **kwargs)

    def _build_url(self, endpoint: str) -> str:
        return f"{self._base_url}/{endpoint.lstrip('/')}"

    def _request(self, method: str, endpoint: str, **kwargs: Any) -> ApiResponse:
        url = self._build_url(endpoint)
        kwargs.setdefault("timeout", self._timeout)

        _logger.info("Request: %s %s", method, url)
        response = self._session.request(method=method, url=url, **kwargs)
        api_response = self._to_api_response(response)
        _logger.info("Response: %s %s -> %s (%.1fms)", method, url, api_response.status_code, api_response.elapsed_ms)

        return api_response

    @staticmethod
    def _to_api_response(response: requests.Response) -> ApiResponse:
        try:
            body: Any = response.json()
        except ValueError:
            body = response.text

        return ApiResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            body=body,
            url=response.url,
            elapsed_ms=response.elapsed.total_seconds() * 1000,
        )