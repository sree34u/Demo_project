"""Page object for the SauceDemo checkout flow (information, overview, complete)."""

from __future__ import annotations

from playwright.sync_api import Page

from locators.checkout_locators import CheckoutLocators
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Encapsulates interactions across the checkout information, overview,
    and completion steps."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def fill_checkout_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill the checkout information step."""
        self.fill(CheckoutLocators.FIRST_NAME_INPUT, first_name)
        self.fill(CheckoutLocators.LAST_NAME_INPUT, last_name)
        self.fill(CheckoutLocators.POSTAL_CODE_INPUT, postal_code)

    def click_continue(self) -> None:
        """Proceed from the information step to the overview step."""
        self.click(CheckoutLocators.CONTINUE_BUTTON)

    def click_cancel(self) -> None:
        """Cancel the current checkout step."""
        self.click(CheckoutLocators.CANCEL_BUTTON)

    def click_finish(self) -> None:
        """Complete the order from the overview step."""
        self.click(CheckoutLocators.FINISH_BUTTON)

    def get_error_message(self) -> str:
        """Return the text of the checkout information error banner."""
        return self.get_text(CheckoutLocators.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """Return True if the checkout information error banner is visible."""
        return self.is_visible(CheckoutLocators.ERROR_MESSAGE)

    def get_subtotal(self) -> float:
        """Return the item subtotal shown on the overview step."""
        text = self.get_text(CheckoutLocators.SUMMARY_SUBTOTAL)
        return float(text.split("$")[-1])

    def get_tax(self) -> float:
        """Return the tax amount shown on the overview step."""
        text = self.get_text(CheckoutLocators.SUMMARY_TAX)
        return float(text.split("$")[-1])

    def get_total(self) -> float:
        """Return the total amount shown on the overview step."""
        text = self.get_text(CheckoutLocators.SUMMARY_TOTAL)
        return float(text.split("$")[-1])

    def get_confirmation_header(self) -> str:
        """Return the confirmation header text on the complete step."""
        return self.get_text(CheckoutLocators.COMPLETE_HEADER)

    def get_confirmation_text(self) -> str:
        """Return the confirmation body text on the complete step."""
        return self.get_text(CheckoutLocators.COMPLETE_TEXT)

    def is_order_complete(self) -> bool:
        """Return True if the order completion header is visible."""
        return self.is_visible(CheckoutLocators.COMPLETE_HEADER)

    def back_to_home(self) -> None:
        """Return to the inventory page from the complete step."""
        self.click(CheckoutLocators.BACK_HOME_BUTTON)