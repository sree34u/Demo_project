"""Root-level pytest configuration.

Registers the shared browser fixture plugin and prunes video recordings for
tests that passed, so only failed-test videos are retained on disk.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pytest
from playwright.sync_api import Page

from utils.logger import get_logger

pytest_plugins = ["fixtures.browser_fixture"]

_logger = get_logger(__name__)

# Maps each test's nodeid to the video path recorded for it and its outcome.
_video_paths_by_test: Dict[str, Path] = {}


@pytest.fixture(autouse=True)
def _track_video_path(page: Page, request: pytest.FixtureRequest):
    """Record the video file path associated with the current test's page."""
    yield
    video = page.video
    if video is not None:
        try:
            _video_paths_by_test[request.node.nodeid] = Path(video.path())
        except Exception:  # noqa: BLE001 - video may not be finalized yet
            pass


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """Delete the recorded video for any test phase that did not fail."""
    if call.when != "call":
        return

    passed = call.excinfo is None
    if not passed:
        return

    video_path = _video_paths_by_test.pop(item.nodeid, None)
    if video_path is None:
        return

    def _cleanup() -> None:
        try:
            if video_path.exists():
                video_path.unlink()
                _logger.info("Deleted video for passed test: %s", video_path)
        except OSError as exc:
            _logger.warning("Could not delete video %s: %s", video_path, exc)

    item.addfinalizer(_cleanup)