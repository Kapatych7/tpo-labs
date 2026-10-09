"""Генерирует коллекцию Postman (формат v2.1) для ЛР5: lab5/TPO_LR5_jsonplaceholder.postman_collection.json"""
import json
from pathlib import Path

def req(name, method, path, tests, body=None):
    r = {"name": name,
         "event": [{"listen": "test", "script": {"type": "text/javascript", "exec": tests.strip().split("\n")}}],
         "request": {"method": method, "header": [{"key": "Content-Type", "value": "application/json; charset=UTF-8"}],
                     "url": {"raw": "{{baseUrl}}" + path, "host": ["{{baseUrl}}"], "path": path.strip("/").split("/")}}}
    if body is not None:
        r["request"]["body"] = {"mode": "raw", "raw": json.dumps(body, ensure_ascii=False, indent=2),
                                "options": {"raw": {"language": "json"}}}
    return r

GET_USER = r"""
pm.test("Статус 200 OK", () => pm.response.to.have.status(200));
pm.test("Время ответа < 2000 мс", () => pm.expect(pm.response.responseTime).to.be.below(2000));
pm.test("Content-Type = JSON", () => pm.expect(pm.response.headers.get("Content-Type")).to.include("application/json"));
const user = pm.response.json();
pm.test("Структура JSON пользователя", () => {
    pm.expect(user).to.have.all.keys("id", "name", "username", "email", "address", "phone", "website", "company");
    pm.expect(user.address).to.include.keys("street", "city", "zipcode", "geo");
    pm.expect(user.company).to.include.keys("name", "catchPhrase", "bs");
});
pm.test("Значения полей", () => {
    pm.expect(user.id).to.eql(1);
    pm.expect(user.name).to.eql("Leanne Graham");
    pm.expect(user.username).to.eql("Bret");
    pm.expect(user.email).to.match(/^[^@\s]+@[^@\s]+\.[^@\s]+$/);
});
pm.collectionVariables.set("userId", user.id);
"""

POST_USER = r"""
const sent = JSON.parse(pm.request.body.raw);
pm.test("Статус 201 Created", () => pm.response.to.have.status(201));
const body = pm.response.json();
pm.test("Ответ содержит новый id", () => {
    pm.expect(body).to.have.property("id");
    pm.expect(body.id).to.be.a("number").and.to.eql(11);
});
pm.test("Поля совпадают с отправленными", () => {
    pm.expect(body.name).to.eql(sent.name);
    pm.expect(body.username).to.eql(sent.username);
    pm.expect(body.email).to.eql(sent.email);
});
"""

PUT_USER = r"""
const sent = JSON.parse(pm.request.body.raw);
pm.test("Статус 200 OK", () => pm.response.to.have.status(200));
const body = pm.response.json();
pm.test("id не изменился", () => pm.expect(body.id).to.eql(Number(pm.collectionVariables.get("userId"))));
pm.test("Поля обновлены", () => {
    pm.expect(body.name).to.eql(sent.name);
    pm.expect(body.email).to.eql(sent.email);
    pm.expect(body.website).to.eql(sent.website);
});
"""

GET_404 = r"""
pm.test("Несуществующий пользователь -> 404", () => pm.response.to.have.status(404));
pm.test("Пустой объект в ответе", () => pm.expect(pm.response.json()).to.eql({}));
"""

GET_POSTS = r"""
pm.test("Статус 200 OK", () => pm.response.to.have.status(200));
const posts = pm.response.json();
pm.test("10 постов пользователя 1", () => {
    pm.expect(posts).to.be.an("array").with.lengthOf(10);
    posts.forEach(p => {
        pm.expect(p.userId).to.eql(1);
        pm.expect(p).to.have.all.keys("userId", "id", "title", "body");
    });
});
"""

coll = {
    "info": {"name": "ТПО ЛР5 — JSONPlaceholder Users",
             "description": "Коллекция запросов к https://jsonplaceholder.typicode.com: GET, POST, PUT + негативный и дополнительный сценарии.",
             "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
    "variable": [{"key": "baseUrl", "value": "https://jsonplaceholder.typicode.com"},
                 {"key": "userId", "value": "1"}],
    "item": [
        req("01 GET — получить пользователя", "GET", "/users/1", GET_USER),
        req("02 POST — создать пользователя", "POST", "/users", POST_USER,
            {"name": "Михаил Герасимов", "username": "mgerasimov", "email": "mikhail@example.com"}),
        req("03 PUT — обновить пользователя", "PUT", "/users/{{userId}}", PUT_USER,
            {"id": 1, "name": "Leanne Graham-Updated", "username": "Bret",
             "email": "leanne.updated@example.com", "website": "tpo-lab.example"}),
        req("04 GET — несуществующий пользователь (негативный)", "GET", "/users/9999", GET_404),
        req("05 GET — посты пользователя (query-параметр)", "GET", "/posts?userId=1", GET_POSTS),
    ],
}
# query-параметр должен быть отдельно
coll["item"][4]["request"]["url"] = {"raw": "{{baseUrl}}/posts?userId=1", "host": ["{{baseUrl}}"],
                                     "path": ["posts"], "query": [{"key": "userId", "value": "1"}]}
out = Path(__file__).with_name("TPO_LR5_jsonplaceholder.postman_collection.json")
out.write_text(json.dumps(coll, ensure_ascii=False, indent=2), encoding="utf-8")
print("Сохранено:", out)
