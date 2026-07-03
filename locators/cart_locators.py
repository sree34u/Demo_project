"""Locators for the SauceDemo cart page."""

from __future__ import annotations


class CartLocators:
    """Selectors for elements on the cart page."""

    CART_ITEM: str = ".cart_item"
    CART_ITEM_NAME: str = ".inventory_item_name"
    CART_ITEM_PRICE: str = ".inventory_item_price"
    CART_ITEM_QUANTITY: str = ".cart_quantity"
    CHECKOUT_BUTTON: str = "#checkout"
    CONTINUE_SHOPPING_BUTTON: str = "#continue-shopping"
    PAGE_TITLE: str = ".title"

    @staticmethod
    def remove_button(product_slug: str) -> str:
        """Return the selector for a cart item's 'Remove' button."""
        return f'[data-test="remove-{product_slug}"]'