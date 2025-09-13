import pytest
from UIFramework.pages.login_page import LoginPage
from UIFramework.config.config import TestConfig



@pytest.mark.framework("selenium")
def test_login_selenium(driver):
    driver.get(TestConfig.base_url)
    login_page = LoginPage(driver)
    login_page.login("student", "Password123")
    assert "Logged In Successfully" in login_page.get_success_message()


@pytest.mark.framework("playwright")
def test_login_playwright(driver):
    driver.goto(TestConfig.base_url)
    login_page = LoginPage(driver)
    login_page.login("student", "Password123")
    assert "Logged In Successfully" in login_page.get_success_message()
