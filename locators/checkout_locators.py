"""Locators for the SauceDemo checkout flow (information, overview, complete)."""

from __future__ import annotations


class CheckoutLocators:
    """Selectors for elements across the checkout steps."""

    FIRST_NAME_INPUT: str = "#first-name"
    LAST_NAME_INPUT: str = "#last-name"
    POSTAL_CODE_INPUT: str = "#postal-code"
    CONTINUE_BUTTON: str = "#continue"
    CANCEL_BUTTON: str = "#cancel"
    FINISH_BUTTON: str = "#finish"
    ERROR_MESSAGE: str = '[data-test="error"]'

    SUMMARY_ITEM: str = ".cart_item"
    SUMMARY_SUBTOTAL: str = ".summary_subtotal_label"
    SUMMARY_TAX: str = ".summary_tax_label"
    SUMMARY_TOTAL: str = ".summary_total_label"

    COMPLETE_HEADER: str = ".complete-header"
    COMPLETE_TEXT: str = ".complete-text"
    BACK_HOME_BUTTON: str = "#back-to-products"