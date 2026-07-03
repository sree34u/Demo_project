"""API tests covering PUT (full update) requests against the /posts resource."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from utils.base_api_client import BaseApiClient

_MAX_RESPONSE_TIME_MS = 3000


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_update_post_with_put_replaces_full_resource(
    api_client: BaseApiClient, api_payloads: Dict[str, Any], post_id: int
) -> None:
    payload = dict(api_payloads["post_update_put"])
    payload["id"] = post_id

    response = api_client.put(f"/posts/{post_id}", json_body=payload)

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS
    assert "application/json" in response.headers.get("Content-Type", "")

    body: Dict[str, Any] = response.body
    assert body["id"] == post_id
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]


@pytest.mark.api
def test_update_non_existent_post_with_put_returns_not_found(
    api_client: BaseApiClient, api_payloads: Dict[str, Any]
) -> None:
    non_existent_id = api_payloads["non_existent_post_id"]
    payload = api_payloads["post_update_put"]

    response = api_client.put(f"/posts/{non_existent_id}", json_body=payload)

    assert response.status_code == 500