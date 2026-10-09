"""Учебное веб-приложение для лабораторных по ТПО.

Разделы:
  /calc     - калькулятор (ЛР1)
  /todo     - список задач с преднамеренными багами (ЛР2)
  /login    - страница входа (ЛР3)
  /contact  - контактная форма (ЛР4)
  /api/...  - простое REST API для нагрузочного теста k6 (ЛР8)

Запуск:  python app.py            (http://127.0.0.1:5000)
"""
import re
import time

from flask import (Flask, jsonify, redirect, render_template, request,
                   session, url_for, abort)

app = Flask(__name__)
app.secret_key = "tpo-labs-demo-key"

# Учётная запись тестового пользователя (тестовые данные для ЛР3)
USERS = {"student": "Passw0rd!"}

SUBJECTS = {
    "question": "Вопрос",
    "order": "Заказ",
    "complaint": "Жалоба",
}

EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")
PHONE_RE = re.compile(r"^\+?\d[\d\s()-]{9,16}$")


@app.route("/")
def index():
    return render_template("index.html")


# ---------- ЛР1: калькулятор ----------
@app.route("/calc")
def calc():
    return render_template("calc.html")


# ---------- ЛР2: Todo ----------
@app.route("/todo")
def todo():
    return render_template("todo.html")


# ---------- ЛР3: логин ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            error = "Введите логин и пароль"
        elif USERS.get(username) != password:
            error = "Неверный логин или пароль"
        else:
            session["user"] = username
            return redirect(url_for("account"))
    return render_template("login.html", error=error)


@app.route("/account")
def account():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("account.html", user=session["user"])


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# ---------- ЛР4: контактная форма ----------
def validate_contact(form):
    errors = {}
    name = form.get("name", "").strip()
    email = form.get("email", "").strip()
    phone = form.get("phone", "").strip()
    subject = form.get("subject", "")
    message = form.get("message", "").strip()
    consent = form.get("consent")

    if not name:
        errors["name"] = "Укажите имя"
    elif len(name) < 2:
        errors["name"] = "Имя должно содержать не менее 2 символов"
    if not email:
        errors["email"] = "Укажите email"
    elif not EMAIL_RE.match(email):
        errors["email"] = "Некорректный email"
    if phone and not PHONE_RE.match(phone):
        errors["phone"] = "Некорректный номер телефона"
    if subject not in SUBJECTS:
        errors["subject"] = "Выберите тему обращения"
    if not message:
        errors["message"] = "Введите сообщение"
    elif len(message) < 10:
        errors["message"] = "Сообщение должно содержать не менее 10 символов"
    if not consent:
        errors["consent"] = "Необходимо согласие на обработку данных"
    return errors


@app.route("/contact", methods=["GET", "POST"])
def contact():
    errors, success, data = {}, None, {}
    if request.method == "POST":
        data = request.form
        errors = validate_contact(request.form)
        if not errors:
            success = f"Спасибо, {data['name'].strip()}! Ваше сообщение отправлено."
            data = {}
    return render_template("contact.html", errors=errors, success=success,
                           data=data, subjects=SUBJECTS)


# ---------- ЛР8: REST API для нагрузочного теста ----------
PRODUCTS = [
    {"id": i, "name": f"Товар {i}", "price": round(99.9 + i * 10.5, 2),
     "in_stock": i % 3 != 0}
    for i in range(1, 51)
]


@app.route("/api/health")
def health():
    return jsonify(status="ok")


@app.route("/api/products")
def products():
    page = max(int(request.args.get("page", 1)), 1)
    size = min(max(int(request.args.get("size", 10)), 1), 50)
    items = PRODUCTS[(page - 1) * size: page * size]
    time.sleep(0.005)  # имитация обращения к БД
    return jsonify(page=page, size=size, total=len(PRODUCTS), items=items)


@app.route("/api/products/<int:pid>")
def product(pid):
    for p in PRODUCTS:
        if p["id"] == pid:
            return jsonify(p)
    abort(404)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)
