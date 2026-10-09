"""ЛР4: автотесты контактной формы по паттерну Page Object."""
import pytest

from lab4.pages.contact_page import ContactPage

pytestmark = pytest.mark.ui

VALID = dict(name="Михаил", email="mikhail@example.com", phone="+7 900 123-45-67",
             subject="question", message="Здравствуйте! Подскажите режим работы.",
             consent=True)


def test_positive_submit_all_fields(driver, base_url):
    """Позитивный: все поля валидны -> сообщение об успешной отправке."""
    page = ContactPage(driver, base_url).open()
    page.fill_form(**VALID).submit()
    assert page.success_text() == "Спасибо, Михаил! Ваше сообщение отправлено."
    assert not page.is_present(page.FORM_ERRORS)


def test_negative_empty_required_name(driver, base_url):
    """Негативный: пустое обязательное поле «Имя» -> текст ошибки, форма не отправлена."""
    page = ContactPage(driver, base_url).open()
    page.fill_form(**{**VALID, "name": ""}).submit()
    assert page.error_for("name") == "Укажите имя"
    assert not page.has_success()


# Тесты по таблице принятия решений (каждая строка таблицы -> отдельный тест)
DECISION_TABLE = [
    # id,        изменения относительно валидных данных,          поле с ошибкой, текст ошибки
    ("R1", {},                                                     None, None),
    ("R2", {"phone": ""},                                          None, None),
    ("R3", {"email": ""},                                          "email", "Укажите email"),
    ("R4", {"email": "mikhail.example.com"},                      "email", "Некорректный email"),
    ("R5", {"phone": "12-ab"},                                     "phone", "Некорректный номер телефона"),
    ("R6", {"subject": ""},                                        "subject", "Выберите тему обращения"),
    ("R7", {"message": "Коротко"},                                 "message", "Сообщение должно содержать не менее 10 символов"),
    ("R8", {"message": ""},                                        "message", "Введите сообщение"),
    ("R9", {"consent": False},                                     "consent", "Необходимо согласие на обработку данных"),
    ("R10", {"name": "М"},                                         "name", "Имя должно содержать не менее 2 символов"),
]


@pytest.mark.parametrize("changes,field,error", [r[1:] for r in DECISION_TABLE],
                         ids=[r[0] for r in DECISION_TABLE])
def test_decision_table(driver, base_url, changes, field, error):
    page = ContactPage(driver, base_url).open()
    page.fill_form(**{**VALID, **changes}).submit()
    if field is None:
        assert page.has_success()
    else:
        assert page.error_for(field) == error
        assert not page.has_success()
