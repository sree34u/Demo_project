"""UI tests for the SauceDemo inventory page: cart badge and sorting."""

from __future__ import annotations

import pytest

from pages.inventory_page import InventoryPage, SortOption
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
def test_add_single_product_updates_cart_badge(inventory_page: InventoryPage) -> None:
    inventory_page.add_product_to_cart(PRODUCT_ONE)

    assert inventory_page.get_cart_badge_count() == 1


@pytest.mark.ui
def test_add_multiple_products_updates_cart_badge(inventory_page: InventoryPage) -> None:
    inventory_page.add_product_to_cart(PRODUCT_ONE)
    inventory_page.add_product_to_cart(PRODUCT_TWO)

    assert inventory_page.get_cart_badge_count() == 2


@pytest.mark.ui
def test_remove_product_from_inventory_updates_cart_badge(inventory_page: InventoryPage) -> None:
    inventory_page.add_product_to_cart(PRODUCT_ONE)
    inventory_page.add_product_to_cart(PRODUCT_TWO)

    inventory_page.remove_product_from_cart(PRODUCT_ONE)

    assert inventory_page.get_cart_badge_count() == 1


@pytest.mark.ui
def test_sort_products_name_z_to_a(inventory_page: InventoryPage) -> None:
    inventory_page.sort_by(SortOption.NAME_Z_TO_A)

    names = inventory_page.get_product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.ui
def test_sort_products_price_low_to_high(inventory_page: InventoryPage) -> None:
    inventory_page.sort_by(SortOption.PRICE_LOW_TO_HIGH)

    prices = inventory_page.get_product_prices()
    assert prices == sorted(prices)