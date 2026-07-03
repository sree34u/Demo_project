"""Page object for the SauceDemo login page."""

from __future__ import annotations

from playwright.sync_api import Page

from locators.login_locators import LoginLocators
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates interactions with the login page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "LoginPage":
        """Navigate to the application root (login page)."""
        self.navigate("")
        return self

    def login(self, username: str, password: str) -> None:
        """Fill credentials and submit the login form."""
        self.fill(LoginLocators.USERNAME_INPUT, username)
        self.fill(LoginLocators.PASSWORD_INPUT, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Return the text of the login error banner."""
        return self.get_text(LoginLocators.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Return True if the login error banner is visible."""
        return self.is_visible(LoginLocators.ERROR_MESSAGE)

    def is_login_page_displayed(self) -> bool:
        """Return True if the login form is still visible."""
        return self.is_visible(LoginLocators.LOGIN_BUTTON)