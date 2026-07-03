"""Locators for the SauceDemo inventory (products) page."""

from __future__ import annotations


class InventoryLocators:
    """Selectors for elements on the inventory page."""

    INVENTORY_LIST: str = ".inventory_list"
    INVENTORY_ITEM: str = ".inventory_item"
    ITEM_NAME: str = ".inventory_item_name"
    ITEM_PRICE: str = ".inventory_item_price"
    ITEM_DESCRIPTION: str = ".inventory_item_desc"
    CART_LINK: str = ".shopping_cart_link"
    CART_BADGE: str = ".shopping_cart_badge"
    SORT_DROPDOWN: str = '[data-test="product-sort-container"]'
    BURGER_MENU_BUTTON: str = "#react-burger-menu-btn"
    LOGOUT_LINK: str = "#logout_sidebar_link"
    PAGE_TITLE: str = ".title"

    @staticmethod
    def add_to_cart_button(product_slug: str) -> str:
        """Return the selector for a product's 'Add to cart' button."""
        return f'[data-test="add-to-cart-{product_slug}"]'

    @staticmethod
    def remove_from_cart_button(product_slug: str) -> str:
        """Return the selector for a product's 'Remove' button."""
        return f'[data-test="remove-{product_slug}"]'