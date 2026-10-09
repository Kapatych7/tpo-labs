# Лабораторные работы по тестированию ПО (ТПО)

[![Run tests](https://github.com/Kapatych7/tpo-labs/actions/workflows/run-tests.yml/badge.svg)](https://github.com/Kapatych7/tpo-labs/actions/workflows/run-tests.yml)

Учебный проект: тестируемые приложения и автотесты к лабораторным работам 1–9.

| Папка | Что внутри |
|---|---|
| `app/` | Учебное веб-приложение на Flask: калькулятор (ЛР1), список задач с багами (ЛР2), вход (ЛР3), обратная связь (ЛР4), REST API (ЛР8) |
| `lab3/` | Selenium: открытие/закрытие браузера, автотесты логина |
| `lab4/` | Page Object (`BasePage`, `ContactPage`), позитивные/негативные тесты формы |
| `lab5/` | Коллекция Postman и тесты API JSONPlaceholder на `requests` + `pytest` |
| `lab6/` | Класс `Calculator` и модульные тесты (`pytest`, `unittest`) |
| `lab7/` | Android-приложение и Appium-тест |
| `lab8/` | Сценарии нагрузочного тестирования k6 |
| `.github/workflows/run-tests.yml` | CI: запуск всех тестов в GitHub Actions (ЛР9) |

## Запуск локально

```bash
pip install -r requirements.txt
python app/app.py          # приложение на http://127.0.0.1:5000
pytest                     # все тесты (UI-тесты сами поднимают приложение)
```
