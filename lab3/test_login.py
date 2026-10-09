"""ЛР3: автотесты страницы логина (Python + Selenium WebDriver + pytest)."""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

VALID_USER = "student"
VALID_PASSWORD = "Passw0rd!"

pytestmark = pytest.mark.ui


def login(driver, base_url, username, password):
    driver.get(f"{base_url}/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-btn").click()


def test_login_page_opens(driver, base_url):
    driver.get(f"{base_url}/login")
    assert "Вход" in driver.title
    assert driver.find_element(By.ID, "username").is_displayed()
    assert driver.find_element(By.ID, "password").get_attribute("type") == "password"


def test_successful_login_shows_logout(driver, base_url):
    """Валидные учётные данные -> переход в кабинет и появление элемента Logout."""
    login(driver, base_url, VALID_USER, VALID_PASSWORD)
    logout = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "logout")))
    assert logout.text == "Logout"
    assert driver.current_url.endswith("/account")
    assert VALID_USER in driver.find_element(By.ID, "welcome").text


@pytest.mark.parametrize("username,password,message", [
    ("student", "wrong", "Неверный логин или пароль"),
    ("nobody", "Passw0rd!", "Неверный логин или пароль"),
    ("", "", "Введите логин и пароль"),
], ids=["wrong_password", "unknown_user", "empty_fields"])
def test_invalid_login_shows_error(driver, base_url, username, password, message):
    login(driver, base_url, username, password)
    flash = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "flash")))
    assert flash.text == message
    assert not driver.find_elements(By.ID, "logout")


def test_logout_returns_to_login(driver, base_url):
    login(driver, base_url, VALID_USER, VALID_PASSWORD)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "logout"))).click()
    WebDriverWait(driver, 5).until(EC.url_contains("/login"))
    assert driver.find_element(By.ID, "login-btn").is_displayed()
