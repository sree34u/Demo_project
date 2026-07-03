"""API tests covering PATCH (partial update) requests against the /posts and /users resources."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from utils.base_api_client import BaseApiClient

_MAX_RESPONSE_TIME_MS = 3000


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_patch_post_updates_only_specified_field(
    api_client: BaseApiClient, api_payloads: Dict[str, Any], post_id: int
) -> None:
    payload = api_payloads["post_update_patch"]

    response = api_client.patch(f"/posts/{post_id}", json_body=payload)

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS

    body: Dict[str, Any] = response.body
    assert body["id"] == post_id
    assert body["title"] == payload["title"]


@pytest.mark.api
def test_patch_user_email(api_client: BaseApiClient, api_payloads: Dict[str, Any]) -> None:
    payload = api_payloads["user_update_patch"]

    response = api_client.patch("/users/1", json_body=payload)

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS

    body: Dict[str, Any] = response.body
    assert body["id"] == 1
    assert body["email"] == payload["email"]