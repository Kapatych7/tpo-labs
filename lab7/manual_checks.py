"""ЛР7: прогон чек-листа мобильного тестирования на эмуляторе Android через adb.

Каждая проверка выполняет действие на эмуляторе (тап, ввод текста, жест, поворот,
звонок/SMS, нехватка памяти и т.д.), сохраняет скриншот в lab7/manual/ и пишет
в лог фактическое состояние экрана. Итог (прошла/не прошла) оценивается по
скриншотам и журналу.

Запуск (эмулятор запущен, приложение установлено):  python3 lab7/manual_checks.py
"""
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from pathlib import Path

PKG = "ru.tpo.notes"
OUT = Path(__file__).parent / "manual"
OUT.mkdir(exist_ok=True)
LOG = []


def adb(*args, check=False):
    r = subprocess.run(["adb", *args], capture_output=True, text=True)
    return r.stdout.strip()


def shell(cmd):
    return adb("shell", cmd)


def log(msg):
    print(msg, flush=True)
    LOG.append(msg)


def shot(name):
    path = OUT / f"{name}.png"
    with open(path, "wb") as f:
        subprocess.run(["adb", "exec-out", "screencap", "-p"], stdout=f)
    log(f"   скриншот: manual/{path.name}")


def dump():
    shell("uiautomator dump /sdcard/ui.xml")
    xml = adb("exec-out", "cat", "/sdcard/ui.xml")
    return ET.fromstring(xml[xml.find("<"):])


def node(rid=None, text=None):
    for n in dump().iter("node"):
        if rid and n.get("resource-id") == f"{PKG}:id/{rid}":
            return n
        if text and n.get("text") == text:
            return n
    return None


def center(n):
    x1, y1, x2, y2 = map(int, re.findall(r"\d+", n.get("bounds")))
    return (x1 + x2) // 2, (y1 + y2) // 2


def tap(rid=None, text=None):
    x, y = center(node(rid, text))
    shell(f"input tap {x} {y}")
    time.sleep(0.8)


def long_press(n, ms=1200):
    x, y = center(n)
    shell(f"input swipe {x} {y} {x} {y} {ms}")
    time.sleep(0.8)


def type_text(t):
    shell(f"input text '{t.replace(' ', '%s')}'")
    time.sleep(0.5)


def counter():
    n = node("counterText")
    return n.get("text") if n is not None else "(нет на экране)"


def items():
    return [n.get("text") for n in dump().iter("node") if n.get("resource-id") == "android:id/text1"]


def add(t):
    tap("noteInput")
    type_text(t)
    tap("addButton")


def is_portrait():
    m = re.search(r"cur=(\d+)x(\d+)", shell("dumpsys window displays"))
    return int(m.group(1)) < int(m.group(2)) if m else True


def set_orientation(portrait=True):
    """Поворот виртуального устройства (как поворот реального телефона)."""
    for _ in range(4):
        if is_portrait() == portrait:
            return
        adb("emu", "rotate")
        time.sleep(2)


def hide_kb():
    """Скрыть экранную клавиатуру, только если она показана (иначе BACK закроет экран)."""
    if "mInputShown=true" in shell("dumpsys input_method"):
        shell("input keyevent 4")
        time.sleep(0.5)


def start_clean():
    shell(f"pm clear {PKG}")
    shell(f"am start -W -n {PKG}/.MainActivity")
    time.sleep(1.5)


def step(num, title):
    log(f"\n[{num}] {title}")


def main():
    shell("settings put system accelerometer_rotation 1")
    set_orientation(portrait=True)
    start_clean()

    step("M01", "Запуск приложения: главный экран, счётчик 0, подсказка «Заметок пока нет»")
    log(f"   счётчик: {counter()}; пустой список: {node(text='Заметок пока нет') is not None}")
    shot("M01_start")

    step("M02", "Тап «Добавить» при пустом поле -> ошибка у поля, заметка не добавлена")
    tap("addButton")
    log(f"   счётчик: {counter()}")
    shot("M02_empty_error")

    step("M03", "Ввод с экранной клавиатуры и добавление заметки")
    add("Kupit moloko")
    add("Sdat laby po TPO")
    log(f"   счётчик: {counter()}; список: {items()}")
    shot("M03_added")

    step("M04", "Ограничение длины: ввод 120 символов -> сохраняется 100")
    tap("noteInput")
    type_text("A" * 120)
    n = node("noteInput")
    log(f"   длина текста в поле: {len(n.get('text'))}")
    tap("addButton")
    hide_kb()
    shot("M04_maxlength")

    step("M05", "Поворот экрана в альбомную ориентацию -> данные и ввод сохраняются")
    tap("noteInput"); type_text("Nedopisannaya")
    set_orientation(portrait=False)
    time.sleep(1)
    n = node("noteInput")
    log(f"   счётчик: {counter()}; текст в поле после поворота: {n.get('text') if n is not None else '—'}")
    shot("M05_landscape")
    set_orientation(portrait=True)
    time.sleep(1)
    hide_kb()
    tap("addButton")  # сохраняем недописанный текст как заметку
    log(f"   после возврата в портрет и сохранения ввода: {counter()}")

    step("M06", "Жест: прокрутка (свайп) длинного списка из 15 заметок")
    tap("clearButton")
    for i in range(1, 16):
        add(f"Zametka {i}")
    hide_kb()
    shot("M06_list_top")
    shell("input swipe 540 1900 540 700 300")
    time.sleep(1)
    vis = items()
    log(f"   видимые элементы после свайпа вверх: {vis[:3]} ... {vis[-2:]}")
    shot("M06_list_scrolled")

    step("M07", "Жест: долгое нажатие на заметку -> удаление и всплывающее сообщение")
    before = counter()
    long_press([n for n in dump().iter("node") if n.get("resource-id") == "android:id/text1"][0])
    log(f"   счётчик до/после: {before} -> {counter()}")
    shot("M07_long_press_delete")

    step("M08", "Прерывание: входящий звонок -> после завершения состояние сохранено")
    before = counter()
    adb("emu", "gsm", "call", "+79001234567")
    time.sleep(3)
    shot("M08_incoming_call")
    adb("emu", "gsm", "cancel", "+79001234567")
    time.sleep(3)
    shell(f"am start -n {PKG}/.MainActivity")
    time.sleep(1.5)
    log(f"   счётчик до/после звонка: {before} -> {counter()}")
    shot("M08_after_call")

    step("M09", "Прерывание: входящее SMS -> уведомление, приложение не теряет данные")
    adb("emu", "sms", "send", "+79001234567", "Test SMS TPO")
    time.sleep(3)
    shot("M09_sms")
    log(f"   счётчик: {counter()}")

    step("M10", "Сворачивание (Home) и возврат через «Недавние» -> состояние сохранено")
    shell("input keyevent 3"); time.sleep(1.5)
    shell(f"am start -n {PKG}/.MainActivity"); time.sleep(1.5)
    log(f"   счётчик: {counter()}")

    step("M11", "Память: система уничтожает активити в фоне («Не сохранять действия») -> данные восстанавливаются")
    shell("settings put global always_finish_activities 1")
    shell(f"am send-trim-memory {PKG} RUNNING_CRITICAL")
    shell("input keyevent 3"); time.sleep(1.5)
    act = shell(f"dumpsys activity activities | grep -c {PKG}/.MainActivity")
    log(f"   записей MainActivity в стеке после ухода в фон: {act}")
    shell(f"am start -W -n {PKG}/.MainActivity"); time.sleep(1.5)
    log(f"   после повторного открытия: {counter()}")
    shot("M11_after_destroy")
    shell("settings put global always_finish_activities 0")

    step("M12", "Память: потребление приложения (dumpsys meminfo)")
    mem = shell(f"dumpsys meminfo {PKG}")
    m = re.search(r"TOTAL PSS:\s+(\d+)", mem) or re.search(r"TOTAL\s+(\d+)", mem)
    log(f"   TOTAL PSS: {m.group(1) if m else '?'} КБ")

    step("M13", "Перезапуск приложения (force-stop) -> заметки сохранены")
    shell(f"am force-stop {PKG}"); time.sleep(1)
    shell(f"am start -W -n {PKG}/.MainActivity"); time.sleep(1.5)
    log(f"   счётчик: {counter()}")

    step("M14", "Крупный шрифт системы (font_scale 1.3) -> интерфейс не обрезается")
    shell("settings put system font_scale 1.3"); time.sleep(2)
    shell(f"am force-stop {PKG}"); shell(f"am start -W -n {PKG}/.MainActivity"); time.sleep(1.5)
    shot("M14_font_large")
    shell("settings put system font_scale 1.0"); time.sleep(1)

    step("M15", "Кнопка «Очистить всё» -> список пуст, счётчик 0")
    shell(f"am force-stop {PKG}"); shell(f"am start -W -n {PKG}/.MainActivity"); time.sleep(1.5)
    tap("clearButton")
    log(f"   счётчик: {counter()}")
    shot("M15_cleared")

    step("M16", "Кнопка «Назад» на главном экране -> приложение закрывается без ошибок")
    shell("input keyevent 4"); time.sleep(1)
    top = shell("dumpsys activity activities | grep -m1 -E 'topResumedActivity|mResumedActivity'")
    log(f"   активное окно: {top.strip()}")

    (OUT / "manual_checks.log").write_text("\n".join(LOG), encoding="utf-8")
    print("\nMANUAL DONE")


if __name__ == "__main__":
    main()
