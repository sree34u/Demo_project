"""Base page object providing common Playwright interactions for all pages."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from playwright.sync_api import Locator, Page

from config.settings import get_settings
from utils.file_utils import ensure_directory
from utils.logger import get_logger

_logger = get_logger(__name__)


class BasePage:
    """Common Playwright actions shared by all concrete page objects."""

    def __init__(self, page: Page) -> None:
        self._page = page
        self._settings = get_settings()
        self._timeout = self._settings.default_timeout_ms

    @property
    def page(self) -> Page:
        return self._page

    def navigate(self, path: str = "") -> None:
        url = path if path.startswith("http") else f"{self._settings.base_url.rstrip('/')}/{path.lstrip('/')}"
        _logger.info("Navigating to %s", url)
        self._page.goto(url, timeout=self._timeout)

    def locator(self, selector: str) -> Locator:
        return self._page.locator(selector)

    def click(self, selector: str) -> None:
        _logger.info("Clicking element: %s", selector)
        self.locator(selector).click(timeout=self._timeout)

    def fill(self, selector: str, value: str) -> None:
        _logger.info("Filling element %s with value", selector)
        self.locator(selector).fill(value, timeout=self._timeout)

    def get_text(self, selector: str) -> str:
        return self.locator(selector).inner_text(timeout=self._timeout)

    def is_visible(self, selector: str) -> bool:
        return self.locator(selector).is_visible()

    def wait_for_selector(self, selector: str, state: str = "visible") -> None:
        self._page.wait_for_selector(selector, state=state, timeout=self._timeout)

    def wait_for_load_state(self, state: str = "load") -> None:
        self._page.wait_for_load_state(state, timeout=self._timeout)

    def get_title(self) -> str:
        return self._page.title()

    def get_current_url(self) -> str:
        return self._page.url

    def screenshot(self, name: str, full_page: bool = True) -> Path:
        directory = ensure_directory(Path(self._settings.screenshot_dir))
        file_path = directory / f"{name}.png"
        self._page.screenshot(path=str(file_path), full_page=full_page)
        _logger.info("Screenshot saved: %s", file_path)
        return file_path

    def reload(self) -> None:
        self._page.reload(timeout=self._timeout)