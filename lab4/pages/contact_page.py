"""Page Object страницы «Обратная связь» (/contact)."""
from selenium.webdriver.common.by import By

from .base_page import BasePage


class ContactPage(BasePage):
    PATH = "/contact"

    NAME = (By.ID, "name")
    EMAIL = (By.ID, "email")
    PHONE = (By.ID, "phone")
    SUBJECT = (By.ID, "subject")
    MESSAGE = (By.ID, "message")
    CONSENT = (By.ID, "consent")
    SUBMIT = (By.ID, "submit-btn")
    SUCCESS = (By.ID, "success-message")
    FORM_ERRORS = (By.ID, "form-errors")

    def fill_form(self, name="", email="", phone="", subject="", message="", consent=False):
        self.type(self.NAME, name)
        self.type(self.EMAIL, email)
        self.type(self.PHONE, phone)
        self.select_by_value(self.SUBJECT, subject)
        self.type(self.MESSAGE, message)
        checkbox = self.find(self.CONSENT)
        if checkbox.is_selected() != consent:
            checkbox.click()
        return self

    def submit(self):
        self.click(self.SUBMIT)
        return self

    def success_text(self):
        return self.text_of(self.SUCCESS)

    def error_for(self, field):
        return self.text_of((By.ID, f"error-{field}"))

    def has_error_for(self, field):
        return self.is_present((By.ID, f"error-{field}"))

    def has_success(self):
        return self.is_present(self.SUCCESS)
