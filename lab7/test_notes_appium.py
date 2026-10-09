"""ЛР7: автотест мобильного приложения «Заметки ТПО» через Appium (UiAutomator2) на эмуляторе Android.

Перед запуском:  appium (сервер на http://127.0.0.1:4723), запущен эмулятор, собран APK.
Запуск:          python3 -m pytest lab7/test_notes_appium.py -v
"""
import os
import time
from pathlib import Path

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

HERE = Path(__file__).parent
APK = os.getenv("APK", str(HERE / "NotesApp/app/build/outputs/apk/debug/app-debug.apk"))
APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")
SHOTS = HERE / "screenshots"
PKG = "ru.tpo.notes"


def rid(name):
    return (AppiumBy.ID, f"{PKG}:id/{name}")


@pytest.fixture(scope="module")
def driver():
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.device_name = "Android Emulator"
    opts.app = APK
    opts.app_package = PKG
    opts.app_activity = ".MainActivity"
    opts.full_reset = False
    opts.no_reset = False          # чистое состояние приложения перед сессией
    opts.set_capability("appium:enforceAppInstall", True)  # всегда ставить свежесобранный APK
    opts.new_command_timeout = 120
    drv = webdriver.Remote(APPIUM_URL, options=opts)
    drv.implicitly_wait(5)
    SHOTS.mkdir(exist_ok=True)
    yield drv
    drv.quit()


def shot(drv, name):
    drv.save_screenshot(str(SHOTS / f"{name}.png"))


def counter(drv):
    return drv.find_element(*rid("counterText")).text


def test_01_app_starts_empty(driver):
    assert driver.current_package == PKG
    assert counter(driver) == "Заметок: 0"
    assert driver.find_element(*rid("emptyText")).is_displayed()
    shot(driver, "01_start")


def test_02_tap_add_with_empty_input_shows_error(driver):
    """Простое действие из задания: тап по кнопке «Добавить» с пустым полем."""
    driver.find_element(*rid("addButton")).click()
    assert counter(driver) == "Заметок: 0"
    shot(driver, "02_empty_error")


def test_03_add_note_by_tap(driver):
    field = driver.find_element(*rid("noteInput"))
    field.send_keys("Купить молоко")
    driver.find_element(*rid("addButton")).click()
    assert counter(driver) == "Заметок: 1"
    items = driver.find_elements(AppiumBy.ID, "android:id/text1")
    assert [i.text for i in items] == ["Купить молоко"]
    assert field.text in ("", "Текст заметки")   # поле очищено (виден hint)
    shot(driver, "03_note_added")


def test_04_rotation_keeps_notes(driver):
    driver.orientation = "LANDSCAPE"
    time.sleep(1.5)
    assert counter(driver) == "Заметок: 1"
    shot(driver, "04_landscape")
    driver.orientation = "PORTRAIT"
    time.sleep(1.5)
    assert counter(driver) == "Заметок: 1"


def test_05_background_and_restore(driver):
    driver.background_app(2)          # сворачивание приложения (прерывание)
    assert counter(driver) == "Заметок: 1"


def test_06_long_press_deletes_note(driver):
    item = driver.find_element(AppiumBy.ID, "android:id/text1")
    driver.execute_script("mobile: longClickGesture", {"elementId": item.id, "duration": 1000})
    time.sleep(0.5)
    assert counter(driver) == "Заметок: 0"
    shot(driver, "06_deleted")
