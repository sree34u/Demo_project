"""API tests covering DELETE requests against the /posts resource."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from utils.base_api_client import BaseApiClient

_MAX_RESPONSE_TIME_MS = 3000


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_delete_post_returns_ok(api_client: BaseApiClient, post_id: int) -> None:
    response = api_client.delete(f"/posts/{post_id}")

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS
    assert "application/json" in response.headers.get("Content-Type", "")
    assert response.body == {}


@pytest.mark.api
def test_delete_non_existent_post_returns_ok(
    api_client: BaseApiClient, api_payloads: Dict[str, Any]
) -> None:
    non_existent_id = api_payloads["non_existent_post_id"]

    response = api_client.delete(f"/posts/{non_existent_id}")

    assert response.status_code == 200