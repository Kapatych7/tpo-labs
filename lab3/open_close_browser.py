"""ЛР3, п.2: инициализация браузера через WebDriver, открытие страницы и закрытие браузера.

Запуск:  python lab3/open_close_browser.py [URL]
"""
import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:5000/login"


def make_driver():
    opts = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "0") == "1":
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1280,900")
    if os.getenv("CHROME_BINARY"):
        opts.binary_location = os.getenv("CHROME_BINARY")
    if os.getenv("CHROMEDRIVER"):
        service = Service(os.getenv("CHROMEDRIVER"))
    else:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def main():
    driver = make_driver()                     # 1. инициализация браузера
    print("Браузер запущен:", driver.capabilities.get("browserVersion"))
    try:
        driver.get(URL)                        # 2. открытие страницы
        print("Открыта страница:", driver.current_url)
        print("Заголовок страницы:", driver.title)
        time.sleep(1)
    finally:
        driver.quit()                          # 3. закрытие браузера
        print("Браузер закрыт")


if __name__ == "__main__":
    main()
