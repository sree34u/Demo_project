"""UI tests for the SauceDemo cart page."""

from __future__ import annotations

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytest_plugins = ["fixtures.browser_fixture"]

STANDARD_USER = "standard_user"
VALID_PASSWORD = "secret_sauce"

PRODUCT_ONE = "Sauce Labs Backpack"
PRODUCT_TWO = "Sauce Labs Bike Light"


@pytest.fixture
def inventory_page(page) -> InventoryPage:
    login_page = LoginPage(page).open()
    login_page.login(STANDARD_USER, VALID_PASSWORD)
    return InventoryPage(page)


@pytest.mark.ui
def test_cart_reflects_added_products(inventory_page: InventoryPage) -> None:
    inventory_page.add_product_to_cart(PRODUCT_ONE)
    inventory_page.add_product_to_cart(PRODUCT_TWO)
    inventory_page.open_cart()

    cart_page = CartPage(inventory_page.page)
    assert cart_page.is_displayed()
    assert cart_page.get_item_count() == 2
    assert set(cart_page.get_cart_item_names()) == {PRODUCT_ONE, PRODUCT_TWO}


@pytest.mark.ui
def test_removing_item_from_cart_updates_item_count(inventory_page: InventoryPage) -> None:
    inventory_page.add_product_to_cart(PRODUCT_ONE)
    inventory_page.add_product_to_cart(PRODUCT_TWO)
    inventory_page.open_cart()

    cart_page = CartPage(inventory_page.page)
    cart_page.remove_item(PRODUCT_ONE)

    assert cart_page.get_item_count() == 1
    assert cart_page.get_cart_item_names() == [PRODUCT_TWO]


@pytest.mark.ui
def test_continue_shopping_returns_to_inventory(inventory_page: InventoryPage) -> None:
    inventory_page.add_product_to_cart(PRODUCT_ONE)
    inventory_page.open_cart()

    cart_page = CartPage(inventory_page.page)
    cart_page.continue_shopping()

    assert inventory_page.is_displayed()
    assert "inventory.html" in inventory_page.get_current_url()