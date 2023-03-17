import unittest
from reed_solomon_code.ReedSolomonCode import ReedSolomonCode


class ReedSolomonCodeTests(unittest.TestCase):

    def test_generator_function(self):
        solomon_15_13 = ReedSolomonCode(4, 1).get_generator()
        solomon_15_11 = ReedSolomonCode(4, 2).get_generator()
        solomon_15_9 = ReedSolomonCode(4, 3).get_generator()
        solomon_15_7 = ReedSolomonCode(4, 4).get_generator()
        self.assertEqual(solomon_15_13, [1, 6, 8])
        self.assertEqual(solomon_15_11, [1, 13, 12, 8, 7])
        self.assertEqual(solomon_15_9, [1, 7, 9, 3, 12, 10, 12])
        self.assertEqual(solomon_15_7, [1, 9, 4, 3, 4, 13, 6, 14, 12])


if __name__ == '__main__':
    unittest.main()
