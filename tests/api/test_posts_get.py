"""API tests covering GET requests against the /posts resource."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from utils.base_api_client import BaseApiClient

_MAX_RESPONSE_TIME_MS = 3000


@pytest.mark.api
def test_get_all_posts_returns_ok(api_client: BaseApiClient) -> None:
    response = api_client.get("/posts")

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.body, list)
    assert len(response.body) == 100


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 2, 3, 26, 100])
def test_get_post_by_id_returns_expected_post(api_client: BaseApiClient, post_id: int) -> None:
    response = api_client.get(f"/posts/{post_id}")

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS

    body: Dict[str, Any] = response.body
    assert body["id"] == post_id
    assert isinstance(body["title"], str) and body["title"]
    assert isinstance(body["body"], str) and body["body"]
    assert isinstance(body["userId"], int)


@pytest.mark.api
def test_get_post_by_non_existent_id_returns_not_found(
    api_client: BaseApiClient, api_payloads: Dict[str, Any]
) -> None:
    non_existent_id = api_payloads["non_existent_post_id"]

    response = api_client.get(f"/posts/{non_existent_id}")

    assert response.status_code == 404


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_comments_for_post_returns_matching_post_id(api_client: BaseApiClient, post_id: int) -> None:
    response = api_client.get("/comments", params={"postId": post_id})

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS
    assert isinstance(response.body, list)
    assert all(comment["postId"] == post_id for comment in response.body)


@pytest.mark.api
def test_get_nested_comments_for_post(api_client: BaseApiClient) -> None:
    response = api_client.get("/posts/1/comments")

    assert response.status_code == 200
    assert isinstance(response.body, list)
    assert all(comment["postId"] == 1 for comment in response.body)