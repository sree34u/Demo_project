"""Playwright/pytest fixtures providing browser, context, and page instances
with video recording, tracing, and screenshot-on-failure support.

This module implements the `pytest_runtest_makereport` hook required to know
whether a test failed at fixture-teardown time. For the hook and fixtures to
be discovered, register this module as a plugin, e.g. in the root
conftest.py:

    pytest_plugins = ["fixtures.browser_fixture"]

or declare the same in individual test modules.
"""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from config.settings import get_settings
from utils.file_utils import ensure_directory
from utils.logger import get_logger

_logger = get_logger(__name__)


def _worker_id() -> str:
    """Return the pytest-xdist worker id, or 'master' when running serially."""
    return os.environ.get("PYTEST_XDIST_WORKER", "master")


def _unique_filename(node_name: str, extension: str) -> str:
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in node_name)
    return f"{safe_name}-{uuid.uuid4().hex[:8]}.{extension}"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator[None, None, None]:
    """Store the outcome of each test phase on the item for use by fixtures."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Provide a single Playwright driver instance for the whole session."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """Launch a single browser instance for the whole session."""
    settings = get_settings()
    browser_launcher = getattr(playwright_instance, settings.browser)
    browser_instance = browser_launcher.launch(headless=settings.headless)
    _logger.info("Launched browser: %s (headless=%s)", settings.browser, settings.headless)
    yield browser_instance
    browser_instance.close()


@pytest.fixture
def context(browser: Browser, request: pytest.FixtureRequest) -> Generator[BrowserContext, None, None]:
    """Provide a fresh, isolated browser context per test with video and tracing."""
    video_dir = ensure_directory(Path("reports") / "videos" / _worker_id())
    browser_context = browser.new_context(
        record_video_dir=str(video_dir),
        viewport={"width": 1920, "height": 1080},
    )
    browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield browser_context

    trace_dir = ensure_directory(Path("reports") / "traces" / _worker_id())
    trace_path = trace_dir / _unique_filename(request.node.name, "zip")
    browser_context.tracing.stop(path=str(trace_path))
    browser_context.close()


@pytest.fixture
def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
    """Provide a fresh page per test and capture a screenshot on failure."""
    page_instance = context.new_page()
    settings = get_settings()

    yield page_instance

    failed = getattr(request.node, "rep_call", None) is not None and request.node.rep_call.failed
    if failed:
        screenshot_dir = ensure_directory(Path(settings.screenshot_dir) / _worker_id())
        screenshot_path = screenshot_dir / _unique_filename(request.node.name, "png")
        try:
            page_instance.screenshot(path=str(screenshot_path), full_page=True)
            _logger.info("Failure screenshot saved: %s", screenshot_path)
        except Exception as exc:  # noqa: BLE001 - best-effort diagnostic capture
            _logger.warning("Failed to capture failure screenshot: %s", exc)

    page_instance.close()