from unittest import TestCase
import math
from numpy import inf, isinf, nan, isnan
from ewaim import calculate

class TestOneNumber(TestCase):
    def test_floats(self):
        for num in range(10):
            self.assertEqual(calculate(str(num) + '**2.0'), pow(num, 2))

    def test_add(self):
        self.assertEqual(2 + 2, 4)
