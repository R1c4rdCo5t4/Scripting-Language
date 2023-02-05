import unittest

import sys
sys.path.insert(0, '../src')

from execution import Execution
from classes import *

class TestExecution(unittest.TestCase): 

    def test_init(self):        
        exe = Execution('test.txt')
        self.assertEqual(exe.file, 'test.txt')
        self.assertEqual(exe.lines[:3], ['set a = 1', 'let b', 'b = a'])
        self.assertEqual(exe.pc, 0)
        self.assertEqual(exe.vars, {})
        

    def test_curr_line(self):
        exe = Execution('test.txt')
        expected_lines = ['set a = 1', 'let b', 'b = a']
        for i, expected_line in enumerate(expected_lines):
            with self.subTest(i=i):
                self.assertEqual(exe.curr_line, expected_line)
                if i >= len(expected_lines) - 1:
                    break
                exe.execute()

    def test_assign_var(self):
        exe = Execution('test.txt')
        exe.assign_var('a', "1")
        self.assertEqual(exe.vars['a'].value, 1)
        self.assertEqual(exe.vars['a'].const, False)
        self.assertEqual(exe.vars['a'].type, 'int')
        exe.assign_var('b', "'hello'", const=True)
        self.assertEqual(exe.vars['b'].value, 'hello')
        self.assertEqual(exe.vars['b'].const, True)
        self.assertEqual(exe.vars['b'].type, 'str')
        self.assertEqual(len(exe.vars), 2)


    def test_convert_ternary(self):
        exe = Execution('test.txt')
        self.assertEqual(exe.convert_ternary('a ? b : c'), 'b if a else c')
        self.assertEqual(exe.convert_ternary('1+1 == 2 ? "true" : "false'), '"true" if 1+1 == 2 else "false')


    def test_substitute_symbols(self):
        exe = Execution('test.txt')
        exe.assign_var('a', 1)
        exe.assign_var('b', 2)
        self.assertEqual(exe.substitute_symbols('a + b'), '1 + 2')
        self.assertEqual(exe.substitute_symbols('a + b + c'), '1 + 2 + c')


    def test_convert_expr(self):
        exe = Execution('test.txt')
        exe.assign_var('a', 1)
        exe.assign_var('b', 2)
        self.assertEqual(exe.convert_expr('a + b'), '1 + 2')
        self.assertEqual(exe.convert_expr('1 ? a : b'), '1 if 1 else 2')


    def test_execute(self):
        
        exe = Execution('test.txt')
        exe.lines.insert(4, "c = 'bye'")
        print(exe.lines)
        with self.subTest('set a = 1'):
            self.assertEqual(exe.pc, 0)
            exe.execute()
            self.assertEqual(exe.vars['a'].value, 1)
            self.assertEqual(exe.vars['a'].const, False)
            self.assertEqual(exe.vars['a'].type, 'int')

        with self.subTest('let b'):
            self.assertEqual(exe.pc, 1)
            exe.execute()
            self.assertEqual(exe.vars['b'].value, None)
            self.assertEqual(exe.vars['b'].const, False)
            self.assertEqual(exe.vars['b'].type, 'NoneType')

        with self.subTest('b = a'):
            self.assertEqual(exe.pc, 2)
            exe.execute()
            self.assertEqual(exe.vars['b'].value, exe.vars['a'].value)
            self.assertEqual(exe.vars['b'].const, exe.vars['a'].const)
            self.assertEqual(exe.vars['b'].type, exe.vars['a'].type) 

        with self.subTest("const c = 'hello'"):
            self.assertEqual(exe.pc, 3)
            exe.execute()
            self.assertEqual(exe.vars['c'].value, 'hello')
            self.assertEqual(exe.vars['c'].const, True)
            self.assertEqual(exe.vars['c'].type, 'str')
     
            with self.assertRaises(Exception):
                exe.execute()
            exe.pc += 1

        with self.subTest('for i from 0 to 5'):
            exe.pc += 1
            exe.execute()
            self.assertNotIn('i', exe.vars)
            self.assertEqual(exe.pc, 8)

        with self.subTest('fn test[x]'):
            exe.pc += 1
            exe.execute()
            self.assertEqual(exe.pc, 11)
            self.assertEqual(exe.functions['test'], Function('test', ['x'], 10))
      
                          
        with self.subTest('test c'):
            exe.execute()
            self.assertEqual(exe.pc, 12)
            exe.execute()

            
        with self.subTest('eof'):
            self.assertTrue(exe.eof)
       
        

if __name__ == '__main__':
    unittest.main()
    

       