"""UI tests for the SauceDemo checkout flow."""

from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytest_plugins = ["fixtures.browser_fixture"]

STANDARD_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"

PRODUCT_ONE = "Sauce Labs Backpack"
PRODUCT_TWO = "Sauce Labs Bike Light"

FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "12345"


@pytest.fixture
def cart_page_with_items(page) -> CartPage:
    login_page = LoginPage(page).open()
    login_page.login(STANDARD_USER, VALID_PASSWORD)

    inventory_page = InventoryPage(page)
    inventory_page.add_product_to_cart(PRODUCT_ONE)
    inventory_page.add_product_to_cart(PRODUCT_TWO)
    inventory_page.open_cart()

    return CartPage(page)


@pytest.mark.ui
def test_checkout_information_missing_fields_shows_error(cart_page_with_items: CartPage) -> None:
    cart_page_with_items.proceed_to_checkout()

    checkout_page = CheckoutPage(cart_page_with_items.page)
    checkout_page.click_continue()

    assert checkout_page.is_error_displayed()


@pytest.mark.ui
def test_checkout_overview_totals_are_consistent(cart_page_with_items: CartPage) -> None:
    cart_page_with_items.proceed_to_checkout()

    checkout_page = CheckoutPage(cart_page_with_items.page)
    checkout_page.fill_checkout_information(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    checkout_page.click_continue()

    subtotal = checkout_page.get_subtotal()
    tax = checkout_page.get_tax()
    total = checkout_page.get_total()

    assert round(subtotal + tax, 2) == round(total, 2)


@pytest.mark.ui
def test_checkout_can_be_cancelled_from_information_step(cart_page_with_items: CartPage) -> None:
    cart_page_with_items.proceed_to_checkout()

    checkout_page = CheckoutPage(cart_page_with_items.page)
    checkout_page.click_cancel()

    assert cart_page_with_items.is_displayed()