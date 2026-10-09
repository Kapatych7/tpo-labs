"""ЛР6: те же проверки на стандартном фреймворке unittest (subTest вместо параметризации)."""
import unittest

from lab6.calculator import Calculator


class CalculatorTest(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        for a, b, expected in [(2, 3, 5), (-2, 3, 1), (0, 0, 0)]:
            with self.subTest(a=a, b=b):
                self.assertEqual(self.calc.add(a, b), expected)

    def test_divide(self):
        for a, b, expected in [(10, 2, 5), (7, 2, 3.5), (-9, 3, -3)]:
            with self.subTest(a=a, b=b):
                self.assertAlmostEqual(self.calc.divide(a, b), expected)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(5, 0)

    def test_is_prime_number(self):
        for n, expected in [(2, True), (17, True), (1, False), (21, False), (-3, False)]:
            with self.subTest(n=n):
                self.assertEqual(self.calc.is_prime_number(n), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
