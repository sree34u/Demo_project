"""API tests covering POST (create) requests against the /posts resource."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from utils.base_api_client import BaseApiClient

_MAX_RESPONSE_TIME_MS = 3000


@pytest.mark.api
def test_create_post_returns_created_with_echoed_body(
    api_client: BaseApiClient, api_payloads: Dict[str, Any]
) -> None:
    payload = api_payloads["post_create"]

    response = api_client.post("/posts", json_body=payload)

    assert response.status_code == 201
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS
    assert "application/json" in response.headers.get("Content-Type", "")

    body: Dict[str, Any] = response.body
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


@pytest.mark.api
def test_create_post_with_partial_payload_still_accepted(
    api_client: BaseApiClient, api_payloads: Dict[str, Any]
) -> None:
    payload = api_payloads["invalid_post_create"]

    response = api_client.post("/posts", json_body=payload)

    assert response.status_code == 201
    body: Dict[str, Any] = response.body
    assert body["body"] == payload["body"]
    assert "id" in body


@pytest.mark.api
def test_create_comment_on_post(api_client: BaseApiClient, api_payloads: Dict[str, Any]) -> None:
    payload = api_payloads["comment_create"]

    response = api_client.post("/comments", json_body=payload)

    assert response.status_code == 201
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS

    body: Dict[str, Any] = response.body
    assert body["postId"] == payload["postId"]
    assert body["email"] == payload["email"]
    assert "id" in body