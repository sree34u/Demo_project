"""UI tests for the SauceDemo login page."""

from __future__ import annotations

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytest_plugins = ["fixtures.browser_fixture"]

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
PERFORMANCE_GLITCH_USER = "performance_glitch_user"
VALID_PASSWORD = "secret_sauce"


@pytest.fixture
def login_page(page) -> LoginPage:
    return LoginPage(page).open()


@pytest.mark.ui
def test_valid_login_redirects_to_inventory(login_page: LoginPage) -> None:
    login_page.login(STANDARD_USER, VALID_PASSWORD)

    inventory_page = InventoryPage(login_page.page)
    assert inventory_page.is_displayed()
    assert "inventory.html" in inventory_page.get_current_url()


@pytest.mark.ui
def test_invalid_login_shows_error(login_page: LoginPage) -> None:
    login_page.login("invalid_user", "wrong_password")

    assert login_page.is_error_displayed()
    assert "do not match" in login_page.get_error_message().lower()


@pytest.mark.ui
def test_locked_out_user_shows_error(login_page: LoginPage) -> None:
    login_page.login(LOCKED_OUT_USER, VALID_PASSWORD)

    assert login_page.is_error_displayed()
    assert "locked out" in login_page.get_error_message().lower()


@pytest.mark.ui
def test_problem_user_can_login(login_page: LoginPage) -> None:
    login_page.login(PROBLEM_USER, VALID_PASSWORD)

    inventory_page = InventoryPage(login_page.page)
    assert inventory_page.is_displayed()
    assert "inventory.html" in inventory_page.get_current_url()


@pytest.mark.ui
def test_performance_glitch_user_can_login(login_page: LoginPage) -> None:
    login_page.login(PERFORMANCE_GLITCH_USER, VALID_PASSWORD)

    inventory_page = InventoryPage(login_page.page)
    assert inventory_page.is_displayed()
    assert "inventory.html" in inventory_page.get_current_url()