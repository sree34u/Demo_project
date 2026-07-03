"""Page object for the SauceDemo inventory (products) page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from locators.inventory_locators import InventoryLocators
from pages.base_page import BasePage


class SortOption:
    """Valid values for the inventory sort dropdown."""

    NAME_A_TO_Z: str = "az"
    NAME_Z_TO_A: str = "za"
    PRICE_LOW_TO_HIGH: str = "lohi"
    PRICE_HIGH_TO_LOW: str = "hihi"


class InventoryPage(BasePage):
    """Encapsulates interactions with the inventory/products page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @staticmethod
    def _to_slug(product_name: str) -> str:
        return product_name.strip().lower().replace(" ", "-")

    def is_displayed(self) -> bool:
        """Return True if the inventory list is visible."""
        return self.is_visible(InventoryLocators.INVENTORY_LIST)

    def add_product_to_cart(self, product_name: str) -> None:
        """Add a product to the cart by its display name."""
        selector = InventoryLocators.add_to_cart_button(self._to_slug(product_name))
        self.click(selector)

    def remove_product_from_cart(self, product_name: str) -> None:
        """Remove a product from the cart by its display name (from inventory view)."""
        selector = InventoryLocators.remove_from_cart_button(self._to_slug(product_name))
        self.click(selector)

    def get_cart_badge_count(self) -> int:
        """Return the number shown on the cart badge, or 0 if not present."""
        if not self.is_visible(InventoryLocators.CART_BADGE):
            return 0
        return int(self.get_text(InventoryLocators.CART_BADGE))

    def open_cart(self) -> None:
        """Navigate to the cart page."""
        self.click(InventoryLocators.CART_LINK)

    def sort_by(self, option_value: str) -> None:
        """Select a sorting option from the dropdown."""
        self.locator(InventoryLocators.SORT_DROPDOWN).select_option(option_value)

    def get_product_names(self) -> List[str]:
        """Return the list of product names in their current display order."""
        return self.locator(InventoryLocators.ITEM_NAME).all_inner_texts()

    def get_product_prices(self) -> List[float]:
        """Return the list of product prices in their current display order."""
        raw_prices = self.locator(InventoryLocators.ITEM_PRICE).all_inner_texts()
        return [float(price.replace("$", "")) for price in raw_prices]

    def logout(self) -> None:
        """Open the side menu and log out."""
        self.click(InventoryLocators.BURGER_MENU_BUTTON)
        self.wait_for_selector(InventoryLocators.LOGOUT_LINK)
        self.click(InventoryLocators.LOGOUT_LINK)