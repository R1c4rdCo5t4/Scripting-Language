import unittest
import sys
sys.path.insert(0, '../src')

from classes import Regex



class TestRegex(unittest.TestCase):

    def setUp(self):
        self.patterns = Regex().patterns
    
    def test_set_regex(self):
        set_pattern = self.patterns['set']
        expr_pattern = self.patterns['expr']

        with self.subTest('set x = 5'):
            
            var_name = set_pattern.search('set x = 5')
            var_value = expr_pattern.search('set x = 5')
            self.assertEqual(var_name.group(1), 'x')
            self.assertEqual(var_value.group(1), '5')

        with self.subTest("set variable = 'hello'"):
            var_name = set_pattern.search("set variable = 'hello'")
            var_value = expr_pattern.search("set variable = 'hello'")
            self.assertEqual(var_name.group(1), 'variable')
            self.assertEqual(var_value.group(1), "'hello'")

        with self.subTest('set x = 5 + 5'):
            var_name = set_pattern.search('set x = 5 + 5')
            var_value = expr_pattern.search('set x = 5 + 5')
            self.assertEqual(var_name.group(1), 'x')
            self.assertEqual(var_value.group(1), '5 + 5')

        with self.subTest('set x'):
            var_name = set_pattern.search('set x')
            var_value = expr_pattern.search('set x')
            self.assertIsNotNone(var_name)
            self.assertIsNone(var_value)


    def test_let(self):
        let_pattern = self.patterns['let']
        
        with self.subTest('let x'):
            var_name = let_pattern.search('let x')
            self.assertEqual(var_name.group(1), 'x')

        with self.subTest("let variable"):
            var_name = let_pattern.search("let variable")
            self.assertEqual(var_name.group(1), 'variable')
       

    def test_const(self):
        const_pattern = self.patterns['const']
        expr_pattern = self.patterns['expr']

        with self.subTest('const x = 5'):
            var_name = const_pattern.search('const x = 5')
            var_value = expr_pattern.search('const x = 5')
            self.assertEqual(var_name.group(1), 'x')
            self.assertEqual(var_value.group(1), '5')

        with self.subTest("const pi = 3.14159"):
            var_name = const_pattern.search("const pi = 3.14159")
            var_value = expr_pattern.search("const pi = 3.14159")
            self.assertEqual(var_name.group(1), 'pi')
            self.assertEqual(var_value.group(1), '3.14159')
        

    def test_reassign(self):
        pass

    def test_fn_call(self):
        pass

    def test_fn_def(self):
        pass

    def test_for(self):
        pass

    def test_expr(self):
        pass





            