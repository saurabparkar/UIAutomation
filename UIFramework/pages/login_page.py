

from UIFramework.pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME = "#username"
    PASSWORD = "#password"
    SUBMIT_BTN = "//button[@id='submit']"
    SUCCESS_TEXT = "//h1[text()='Logged In Successfully']"

    def login(self, username: str, password: str):
        self.enter_text(self.USERNAME, username)
        self.enter_text(self.PASSWORD, password)
        self.click_object(self.SUBMIT_BTN)

    def get_success_message(self) -> str:
        return self.get_text(self.SUCCESS_TEXT)
