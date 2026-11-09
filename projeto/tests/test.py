import sys
import unittest
from array import array
from itertools import product
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from heap import heap_unique
from bitmap import bitmap_unique


class Corretude(unittest.TestCase):
    def check_case(self, values):
        original = array('H', values)
        expected = set(original)
        for algorithm in [heap_unique, bitmap_unique]:
            a = array('H', original)
            u = algorithm(a)
            result = list(a[:u])
            self.assertEqual(len(a), len(original))
            self.assertEqual(u, len(expected))
            self.assertEqual(set(result), expected)
            self.assertEqual(len(result), len(set(result)))
            if algorithm is heap_unique:
                self.assertEqual(result, sorted(expected))
            else:
                self.assertEqual(result, list(dict.fromkeys(original)))

    def test_examples(self):
        for values in [[], [42], [7]*8, [0,65535], [3,1,3,0,65535,1], list(range(10)), list(range(9,-1,-1))]:
            self.check_case(values)

    def test_exhaustive(self):
        for n in range(8):
            for values in product([0,64,65535], repeat=n):
                self.check_case(values)

    def test_domain(self):
        self.check_case(range(65536))
        self.check_case(range(65535,-1,-1))


if __name__ == '__main__':
    unittest.main(verbosity=2)
