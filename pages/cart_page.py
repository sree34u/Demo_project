"""Page object for the SauceDemo cart page."""

from __future__ import annotations

from typing import List

from playwright.sync_api import Page

from locators.cart_locators import CartLocators
from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates interactions with the cart page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @staticmethod
    def _to_slug(product_name: str) -> str:
        return product_name.strip().lower().replace(" ", "-")

    def is_displayed(self) -> bool:
        """Return True if the cart page title is visible."""
        return self.is_visible(CartLocators.PAGE_TITLE)

    def get_cart_item_names(self) -> List[str]:
        """Return the names of all products currently in the cart."""
        return self.locator(CartLocators.CART_ITEM_NAME).all_inner_texts()

    def get_cart_item_prices(self) -> List[float]:
        """Return the prices of all products currently in the cart."""
        raw_prices = self.locator(CartLocators.CART_ITEM_PRICE).all_inner_texts()
        return [float(price.replace("$", "")) for price in raw_prices]

    def get_item_count(self) -> int:
        """Return the number of line items in the cart."""
        return self.locator(CartLocators.CART_ITEM).count()

    def remove_item(self, product_name: str) -> None:
        """Remove a product from the cart by its display name."""
        selector = CartLocators.remove_button(self._to_slug(product_name))
        self.click(selector)

    def continue_shopping(self) -> None:
        """Return to the inventory page."""
        self.click(CartLocators.CONTINUE_SHOPPING_BUTTON)

    def proceed_to_checkout(self) -> None:
        """Start the checkout flow."""
        self.click(CartLocators.CHECKOUT_BUTTON)