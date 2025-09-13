import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from playwright.sync_api import Page, sync_playwright
from UIFramework.config.config import TestConfig


# @pytest.fixture(scope="session")
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="uat", help="Choose an environment")
    parser.addoption("--browser", action="store", default="Chrome", help="Choose an browser")
    parser.addoption("--headless", action="store_true", default=False, help="Run in headless mode")


@pytest.fixture(scope="session")
def config(request):
    return {
        "env": request.config.getoption("--env").lower(),
        "browser": request.config.getoption("--browser").lower(),
        "headless": request.config.getoption("--headless")
    }

class UnifiedDriver:
    def __init__(self, backend, instance):
        self.backend = backend  # "selenium" or "playwright"
        self.instance = instance

    def open_url(self, url):
        if self.backend == "selenium":
            self.instance.get(url)
        elif self.backend == "playwright":
            self.instance.goto(url)

    def quit(self):
        if self.backend == "selenium":
            self.instance.quit()
        elif self.backend == "playwright":
            self.instance.context.close()
            self.instance.browser.close()

@pytest.fixture(scope="function")
def driver(config, request):

    framework_marker = request.node.get_closest_marker("framework")
    framework = framework_marker.args[0].lower() if framework_marker else "selenium"
    env = config["env"]
    browser = config["browser"]
    headless = config["headless"]
    base_url = TestConfig.base_url

    if framework == "selenium":
        selenium_browsers = {
                "chrome": lambda: webdriver.Chrome(options=_chrome_opts(headless)),
                "firefox": lambda: webdriver.Firefox(options=_firefox_opts(headless))
        }

        if browser not in selenium_browsers:
            raise ValueError(f"Unsupported Selenium browser: {browser}")
        driver = selenium_browsers[browser]()
        driver.get(base_url)
        yield driver
        driver.quit()
    elif framework == "playwright":
        pw = sync_playwright().start()
        playwright_browsers = {
            "chrome": lambda: pw.chromium.launch(headless=headless),
            "firefox": pw.firefox.launch(headless=headless)
            }
        if browser not in playwright_browsers:
            raise ValueError(f"Unsupported Selenium browser: {browser}")
        context = browser.new_context()
        page = context.new_page()
        page.goto(base_url)
        yield page
        context.close()
        browser.close()
        pw.stop()
    else:
        raise ValueError(f"Unknown framework: {framework}")


def _chrome_opts(headless: bool):
    opts = ChromeOptions()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    return opts


def _firefox_opts(headless: bool):
    opts = FirefoxOptions()
    if headless:
        opts.add_argument("--headless")
    return opts


