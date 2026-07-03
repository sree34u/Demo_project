"""Locators for the SauceDemo login page."""

from __future__ import annotations


class LoginLocators:
    """Selectors for elements on the login page."""

    USERNAME_INPUT: str = "#user-name"
    PASSWORD_INPUT: str = "#password"
    LOGIN_BUTTON: str = "#login-button"
    ERROR_MESSAGE: str = '[data-test="error"]'
    ERROR_BUTTON: str = ".error-button"
    LOGIN_LOGO: str = ".login_logo"