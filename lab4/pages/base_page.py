"""Базовый класс Page Object: общие действия со страницей."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class BasePage:
    PATH = "/"

    def __init__(self, driver, base_url, timeout=5):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.base_url + self.PATH)
        return self

    @property
    def title(self):
        return self.driver.title

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        el = self.find(locator)
        el.clear()
        if text:
            el.send_keys(text)

    def select_by_value(self, locator, value):
        Select(self.find(locator)).select_by_value(value)

    def text_of(self, locator):
        return self.visible(locator).text

    def is_present(self, locator):
        return len(self.driver.find_elements(*locator)) > 0

    @staticmethod
    def by_id(element_id):
        return (By.ID, element_id)
