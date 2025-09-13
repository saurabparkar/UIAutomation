import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from playwright.sync_api import Page

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class BasePage:
    def __init__(self, browser_obj, timeout: int = 10):
        self.browser_obj = browser_obj
        self.timeout = timeout

    def _resolve_locator(self, locator: str):
        """Return correct locator for Selenium, or raw string for Playwright"""
        if isinstance(self.browser_obj, WebDriver):
            if locator.startswith("//") or locator.startswith("(//"):
                return By.XPATH, locator
            return By.CSS_SELECTOR, locator
        return locator

    def click_object(self, locator: str):
        try:
            if isinstance(self.browser_obj, WebDriver):
                resolved = self._resolve_locator(locator)
                WebDriverWait(self.browser_obj, self.timeout).until(
                    EC.element_to_be_clickable(resolved)
                ).click()
            elif isinstance(self.browser_obj, Page):
                self.browser_obj.locator(locator).click(timeout=self.timeout * 1000)
            logging.info(f"Clicked element: {locator}")
        except Exception as e:
            logging.error(f"Click failed for {locator}: {e}")
            raise

    def enter_text(self, locator: str, value: str):
        try:
            if isinstance(self.browser_obj, WebDriver):
                resolved = self._resolve_locator(locator)
                element = WebDriverWait(self.browser_obj, self.timeout).until(
                    EC.presence_of_element_located(resolved)
                )
                element.clear()
                element.send_keys(value)
            elif isinstance(self.browser_obj, Page):
                self.browser_obj.locator(locator).fill(value, timeout=self.timeout * 1000)
            logging.info(f"Entered text '{value}' in {locator}")
        except Exception as e:
            logging.error(f"Enter text failed for {locator}: {e}")
            raise

    def get_text(self, locator: str) -> str:
        try:
            if isinstance(self.browser_obj, WebDriver):
                resolved = self._resolve_locator(locator)
                element = WebDriverWait(self.browser_obj, self.timeout).until(
                    EC.visibility_of_element_located(resolved)
                )
                text = element.text
            elif isinstance(self.browser_obj, Page):
                text = self.browser_obj.locator(locator).inner_text(timeout=self.timeout * 1000)
            logging.info(f"Text from {locator}: {text}")
            return text
        except Exception as e:
            logging.error(f"Get text failed for {locator}: {e}")
            raise
