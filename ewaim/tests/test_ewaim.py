from unittest import TestCase
import math
from numpy import inf, isinf, nan, isnan
from ewaim import calculate
from ewaim import get_csv
from ewaim import mean_lat_long

class TestOneNumber(TestCase):
    def test_floats(self):
        for num in range(10):
            self.assertEqual(calculate(str(num) + '**2.0'), pow(num, 2))

    def test_add(self):
        self.assertEqual(2 + 2, 4)

    def test_latlong(self):
        foo_latlong = mean_lat_long("tester")
        self.assertEqual(foo_latlong, mean_lat_long("tester"))
