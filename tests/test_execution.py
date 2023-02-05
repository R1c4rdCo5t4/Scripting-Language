import unittest

import sys
sys.path.insert(0, '../src')

from execution import Execution


with open('test.txt', 'w') as f:
    f.write('set a = 1\nlet b\n\nb = a\n')

exe = Execution('test.txt')


class TestExecution(unittest.TestCase): 

    def test_1_init(self):        
        exe.pc = 0
        self.assertEqual(exe.file, 'test.txt')
        self.assertEqual(exe.lines, ['set a = 1', 'let b', '', 'b = a'])
        self.assertEqual(exe.pc, 0)
        self.assertEqual(exe.vars, {})
        

    def test_2_curr_line(self):
        exe.pc = 0
        expected_lines = ['set a = 1', 'let b', '', 'b = a']
        for i, expected_line in enumerate(expected_lines):
            with self.subTest(i=i):
                self.assertEqual(exe.curr_line, expected_line)
                if i >= len(expected_lines) - 1:
                    break
                exe.execute()


    def test_3_eof(self):
        self.assertFalse(exe.eof)
        exe.execute()
        self.assertTrue(exe.eof)
        

    def test_assign_var(self):
        pass

    def test_convert_ternary(self):
        pass

    def test_substitute_vars(self):
        pass

    def test_convert_expr(self):
        pass

    def test_search_line_expr(self):
        pass

    def test_execute(self):
        pass




if __name__ == '__main__':
    unittest.main()