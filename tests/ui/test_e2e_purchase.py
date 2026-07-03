"""End-to-end UI test covering the full SauceDemo purchase journey."""

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

FIRST_NAME = "Jane"
LAST_NAME = "Smith"
POSTAL_CODE = "94107"


@pytest.mark.ui
def test_end_to_end_purchase_flow(page) -> None:
    login_page = LoginPage(page).open()
    login_page.login(STANDARD_USER, VALID_PASSWORD)

    inventory_page = InventoryPage(page)
    assert inventory_page.is_displayed()

    inventory_page.add_product_to_cart(PRODUCT_ONE)
    inventory_page.add_product_to_cart(PRODUCT_TWO)
    assert inventory_page.get_cart_badge_count() == 2

    inventory_page.open_cart()
    cart_page = CartPage(page)
    assert cart_page.get_item_count() == 2

    cart_page.proceed_to_checkout()
    checkout_page = CheckoutPage(page)
    checkout_page.fill_checkout_information(FIRST_NAME, LAST_NAME, POSTAL_CODE)
    checkout_page.click_continue()

    assert round(checkout_page.get_subtotal() + checkout_page.get_tax(), 2) == round(
        checkout_page.get_total(), 2
    )

    checkout_page.click_finish()

    assert checkout_page.is_order_complete()
    assert "thank you" in checkout_page.get_confirmation_header().lower()

    checkout_page.back_to_home()
    assert inventory_page.is_displayed()