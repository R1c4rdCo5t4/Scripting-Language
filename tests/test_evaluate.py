import unittest
import sys
sys.path.insert(0, '../src')

from evaluate import *



class TestEvaluate(unittest.TestCase):


    def test_empty_expression(self):
        self.assertIsNone(evaluate('', {}))
        self.assertIsNone(evaluate('None', {}))

    def test_basic_arithmetic(self):
        self.assertEqual(evaluate('1 + 2', {}), 3)
        self.assertEqual(evaluate('2 - 1', {}), 1)
        self.assertEqual(evaluate('2 * 3', {}), 6)
        self.assertEqual(evaluate('6 / 2', {}), 3)
        self.assertEqual(evaluate('2 ** 3', {}), 8)
        self.assertEqual(evaluate('7 % 3', {}), 1)
        self.assertEqual(evaluate('-2', {}), -2)
        self.assertEqual(evaluate('7 // 3', {}), 2)

    def test_comparisons(self):
        self.assertEqual(evaluate('2 == 2', {}), True)
        self.assertEqual(evaluate('2 != 3', {}), True)
        self.assertEqual(evaluate('2 < 3', {}), True)
        self.assertEqual(evaluate('2 <= 3', {}), True)
        self.assertEqual(evaluate('2 > 3', {}), False)
        self.assertEqual(evaluate('2 >= 3', {}), False)
        

    def test_if_expression(self):
        self.assertEqual(evaluate('2 if 2 == 2 else 3', {}), 2)
        self.assertEqual(evaluate('2 if 3 == 4 else 3', {}), 3)

    def test_string_concatenation(self):
        self.assertEqual(evaluate('"hello" + " " + "world"', {}), 'hello world')

    def test_undefined_variable(self):
        with self.assertRaises(Error) as cm:
            evaluate('x + 2', {})
        self.assertEqual(str(cm.exception), "undefined variable 'x'")
       

if __name__ == '__main__':
    unittest.main()