"""ЛР5: тесты REST API JSONPlaceholder на Python (requests + pytest).
Повторяют проверки из коллекции Postman TPO_LR5_jsonplaceholder.postman_collection.json."""
import os
import re

import pytest
import requests

BASE_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com")
HEADERS = {"Content-Type": "application/json; charset=UTF-8"}
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

pytestmark = pytest.mark.api


@pytest.fixture(scope="module")
def session():
    s = requests.Session()
    s.headers.update(HEADERS)
    yield s
    s.close()


def test_get_user(session):
    r = session.get(f"{BASE_URL}/users/1", timeout=10)
    assert r.status_code == 200
    assert r.elapsed.total_seconds() < 2
    assert "application/json" in r.headers["Content-Type"]
    user = r.json()
    assert set(user) == {"id", "name", "username", "email", "address", "phone", "website", "company"}
    assert {"street", "city", "zipcode", "geo"} <= set(user["address"])
    assert {"name", "catchPhrase", "bs"} <= set(user["company"])
    assert user["id"] == 1
    assert user["name"] == "Leanne Graham"
    assert user["username"] == "Bret"
    assert EMAIL_RE.match(user["email"])


def test_create_user(session):
    payload = {"name": "Михаил Герасимов", "username": "mgerasimov", "email": "mikhail@example.com"}
    r = session.post(f"{BASE_URL}/users", json=payload, timeout=10)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] == 11
    for key, value in payload.items():
        assert body[key] == value


def test_update_user(session):
    payload = {"id": 1, "name": "Leanne Graham-Updated", "username": "Bret",
               "email": "leanne.updated@example.com", "website": "tpo-lab.example"}
    r = session.put(f"{BASE_URL}/users/1", json=payload, timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 1
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]
    assert body["website"] == payload["website"]


def test_get_missing_user_returns_404(session):
    r = session.get(f"{BASE_URL}/users/9999", timeout=10)
    assert r.status_code == 404
    assert r.json() == {}


@pytest.mark.parametrize("user_id", [1, 2, 5])
def test_posts_of_user(session, user_id):
    r = session.get(f"{BASE_URL}/posts", params={"userId": user_id}, timeout=10)
    assert r.status_code == 200
    posts = r.json()
    assert len(posts) == 10
    for p in posts:
        assert p["userId"] == user_id
        assert set(p) == {"userId", "id", "title", "body"}
