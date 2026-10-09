"""ЛР6: модульные тесты класса Calculator (pytest, параметризация)."""
import math

import pytest

from lab6.calculator import Calculator


@pytest.fixture
def calc():
    return Calculator()


# ---------- add ----------
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-2, -3, -5),
    (-2, 3, 1),
    (0, 0, 0),
    (10**12, 1, 10**12 + 1),
])
def test_add_integers(calc, a, b, expected):
    assert calc.add(a, b) == expected


@pytest.mark.parametrize("a,b,expected", [(0.1, 0.2, 0.3), (1.5, 2.25, 3.75), (-0.5, 0.5, 0.0)])
def test_add_floats(calc, a, b, expected):
    assert calc.add(a, b) == pytest.approx(expected)


# ---------- subtract / multiply ----------
@pytest.mark.parametrize("a,b,expected", [(5, 3, 2), (3, 5, -2), (0, 7, -7), (2.5, 0.5, 2.0)])
def test_subtract(calc, a, b, expected):
    assert calc.subtract(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a,b,expected", [(4, 5, 20), (-4, 5, -20), (-4, -5, 20), (7, 0, 0), (0.5, 0.5, 0.25)])
def test_multiply(calc, a, b, expected):
    assert calc.multiply(a, b) == pytest.approx(expected)


# ---------- divide ----------
@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5),
    (7, 2, 3.5),
    (-9, 3, -3),
    (0, 5, 0),
    (1, 3, 1 / 3),
])
def test_divide(calc, a, b, expected):
    assert calc.divide(a, b) == pytest.approx(expected)


@pytest.mark.parametrize("a", [1, 0, -5, 2.5])
def test_divide_by_zero_raises(calc, a):
    with pytest.raises(ZeroDivisionError, match="Деление на ноль"):
        calc.divide(a, 0)


def test_divide_by_float_zero_raises(calc):
    with pytest.raises(ZeroDivisionError):
        calc.divide(1, 0.0)


# ---------- is_prime_number ----------
@pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 97, 7919])
def test_is_prime_true(calc, n):
    assert calc.is_prime_number(n) is True


@pytest.mark.parametrize("n", [-7, 0, 1, 4, 9, 15, 25, 100, 7917])
def test_is_prime_false(calc, n):
    assert calc.is_prime_number(n) is False


@pytest.mark.parametrize("n", [2.0, "7", None])
def test_is_prime_rejects_non_integers(calc, n):
    with pytest.raises(TypeError):
        calc.is_prime_number(n)


# ---------- проверка типов ----------
@pytest.mark.parametrize("method", ["add", "subtract", "multiply", "divide"])
@pytest.mark.parametrize("bad", ["2", None, True, [1]])
def test_methods_reject_non_numbers(calc, method, bad):
    with pytest.raises(TypeError):
        getattr(calc, method)(bad, 1)


def test_add_infinity(calc):
    assert math.isinf(calc.add(math.inf, 1))
