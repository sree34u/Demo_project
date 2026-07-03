"""API tests covering GET requests against the /users resource."""

from __future__ import annotations

from typing import Any, Dict

import pytest

from utils.base_api_client import BaseApiClient

_MAX_RESPONSE_TIME_MS = 3000
_REQUIRED_USER_FIELDS = ("id", "name", "username", "email", "address", "phone", "website", "company")


@pytest.mark.api
def test_get_all_users_returns_ok(api_client: BaseApiClient) -> None:
    response = api_client.get("/users")

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS
    assert "application/json" in response.headers.get("Content-Type", "")
    assert isinstance(response.body, list)
    assert len(response.body) == 10


@pytest.mark.api
@pytest.mark.parametrize("user_id", [1, 2, 5, 10])
def test_get_user_by_id_returns_expected_fields(api_client: BaseApiClient, user_id: int) -> None:
    response = api_client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.elapsed_ms < _MAX_RESPONSE_TIME_MS

    body: Dict[str, Any] = response.body
    assert body["id"] == user_id
    for field in _REQUIRED_USER_FIELDS:
        assert field in body


@pytest.mark.api
def test_get_user_by_non_existent_id_returns_not_found(api_client: BaseApiClient) -> None:
    response = api_client.get("/users/99999")

    assert response.status_code == 404