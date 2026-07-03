"""Shared fixtures for API tests targeting the JSONPlaceholder service."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pytest

from utils.base_api_client import BaseApiClient
from utils.file_utils import read_json

_JSONPLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"
_PAYLOADS_PATH = Path(__file__).resolve().parent.parent.parent / "testdata" / "api_payloads.json"


@pytest.fixture(scope="session")
def api_client() -> BaseApiClient:
    """Provide a BaseApiClient configured for the JSONPlaceholder API."""
    client = BaseApiClient(base_url=_JSONPLACEHOLDER_BASE_URL)
    yield client
    client.close()


@pytest.fixture(scope="session")
def api_payloads() -> Dict[str, Any]:
    """Provide reusable request payloads and test data values."""
    return read_json(_PAYLOADS_PATH)