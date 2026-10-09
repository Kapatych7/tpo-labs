"""Общие фикстуры pytest для UI-тестов (ЛР3, ЛР4, ЛР9).

* app_server - поднимает учебное Flask-приложение из папки app/ в отдельном потоке;
* base_url   - адрес приложения (можно переопределить переменной BASE_URL);
* driver     - браузер Chrome через Selenium WebDriver.

Драйвер браузера ищется так:
  1) переменные окружения CHROMEDRIVER / CHROME_BINARY (если заданы);
  2) webdriver-manager (скачивает подходящий chromedriver);
  3) встроенный Selenium Manager.
"""
import os
import sys
import threading
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

ROOT = Path(__file__).parent
SCREENSHOTS = ROOT / "screenshots"
sys.path.insert(0, str(ROOT / "app"))


@pytest.fixture(scope="session")
def base_url():
    if os.getenv("BASE_URL"):
        yield os.getenv("BASE_URL").rstrip("/")
        return
    from werkzeug.serving import make_server
    from app import app as flask_app

    server = make_server("127.0.0.1", 5055, flask_app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:5055"
    server.shutdown()


def _chrome_options():
    opts = webdriver.ChromeOptions()
    if os.getenv("HEADLESS", "1") == "1":
        opts.add_argument("--headless=new")
    for arg in ("--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900",
                "--lang=ru-RU"):
        opts.add_argument(arg)
    if os.getenv("CHROME_BINARY"):
        opts.binary_location = os.getenv("CHROME_BINARY")
    return opts


def create_driver():
    opts = _chrome_options()
    if os.getenv("CHROMEDRIVER"):
        return webdriver.Chrome(service=Service(os.getenv("CHROMEDRIVER")), options=opts)
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)
    except Exception as exc:  # нет доступа к сети и т.п.
        print(f"webdriver-manager недоступен ({exc}); используется Selenium Manager")
        return webdriver.Chrome(options=opts)


@pytest.fixture
def driver(request):
    drv = create_driver()
    drv.implicitly_wait(2)
    yield drv
    SCREENSHOTS.mkdir(exist_ok=True)
    drv.save_screenshot(str(SCREENSHOTS / f"{request.node.name}.png"))
    drv.quit()
