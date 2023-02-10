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
        
        reassign_pattern = self.patterns['reassign']
        expr_pattern = self.patterns['expr']

        with self.subTest('x = 5'):
            var_name = reassign_pattern.search('x = 5')
            var_value = expr_pattern.search('x = 5')
            self.assertEqual(var_name.group(1), 'x')
            self.assertEqual(var_value.group(1), '5')

        with self.subTest("variable = 'hello'"):
            var_name = reassign_pattern.search("variable = 'hello'")
            var_value = expr_pattern.search("variable = 'hello'")
            self.assertEqual(var_name.group(1), 'variable')
            self.assertEqual(var_value.group(1), "'hello'")

        with self.subTest('x = 5 + 5'):
            var_name = reassign_pattern.search('x = 5 + 5')
            var_value = expr_pattern.search('x = 5 + 5')
            self.assertEqual(var_name.group(1), 'x')
            self.assertEqual(var_value.group(1), '5 + 5')

       

    def test_fn_call(self):
        
        fn_call_pattern = self.patterns['fn_call']

        with self.subTest('print 5'):
            fn = fn_call_pattern.search('print 5')
            self.assertEqual(fn.group(1), 'print')
            self.assertEqual(fn.group(2), '5')

        with self.subTest("log 'hello', 5"):
            fn = fn_call_pattern.search("log 'hello', 5")
            self.assertEqual(fn.group(1), 'log')
            self.assertEqual(fn.group(2), "'hello', 5")
 

    def test_fn_def(self):
        
        fn_def_pattern = self.patterns['fn_def']
        with self.subTest('fn my_fn[x, y]'):
            fn = fn_def_pattern.search('fn my_fn[x, y]')
            self.assertEqual(fn.group(1), 'my_fn')
            self.assertEqual(fn.group(2), 'x, y')


    def test_for(self):
        
        for_pattern = self.patterns['for']
        with self.subTest('for i from 0 to 10'):
            fn = for_pattern.search('for i from 0 to 10')
            self.assertEqual(fn.group(1), 'i')
            self.assertEqual(fn.group(2), '0')
            self.assertEqual(fn.group(3), '10')

        with self.subTest('for j from 0 to 10 step 2'):
            fn = for_pattern.search('for j from 0 to 10 step 2')
            self.assertEqual(fn.group(1), 'j')
            self.assertEqual(fn.group(2), '0')
            self.assertEqual(fn.group(3), '10')
            self.assertEqual(fn.group(5), '2')








            