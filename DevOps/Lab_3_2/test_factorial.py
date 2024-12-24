import unittest
from factorial import factorial


class TestFactorial(unittest.TestCase):

    def test_factorial_of_positive_numbers(self):
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(6), 720)
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(1), 1)

    def test_factorial_of_negative_numbers(self):
        with self.assertRaises(ValueError):
            factorial(-1)


if __name__ == "__main__":
    unittest.main()
