import unittest

import sys
sys.path.insert(0, '../src')

from execution import Execution as exe

exe = exe('test.txt')

class TestExecution(unittest.TestCase):

    def test_init(self):
        self.assertEqual(exe.file, 'test.txt')
        self.assertEqual(exe.lines, ['set a = 1', 'set b = 2', '', 'set c = a + b'])
        self.assertEqual(exe.pc, 0)
        self.assertEqual(exe.vars, {})


    def test_curr_line(self):
        pass

    def test_eof(self):
        pass

    def test_ignore_line(self):
        pass

    def test_ignore_lines(self):
        pass

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