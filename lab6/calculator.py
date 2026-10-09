"""ЛР6: класс Calculator с бизнес-логикой (объект модульного тестирования)."""
import math
from numbers import Real


class Calculator:
    """Простой калькулятор. Аргументы - числа int/float (bool не допускается)."""

    @staticmethod
    def _check(*values):
        for v in values:
            if isinstance(v, bool) or not isinstance(v, Real):
                raise TypeError(f"Ожидалось число, получено {type(v).__name__}")

    def add(self, a, b):
        self._check(a, b)
        return a + b

    def subtract(self, a, b):
        self._check(a, b)
        return a - b

    def multiply(self, a, b):
        self._check(a, b)
        return a * b

    def divide(self, a, b):
        self._check(a, b)
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return a / b

    def is_prime_number(self, n):
        """True, если n - простое натуральное число."""
        if isinstance(n, bool) or not isinstance(n, int):
            raise TypeError("Проверять на простоту можно только целые числа")
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False
        for d in range(3, math.isqrt(n) + 1, 2):
            if n % d == 0:
                return False
        return True
