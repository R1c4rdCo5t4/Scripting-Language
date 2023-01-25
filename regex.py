import re
from enum import Enum


class Regex(Enum):
    VAR_NAME = re.compile(r"set\s+(\w+)")
    RIGHT_SIDE = re.compile(r"\s*=\s*(.+)")
    FUNC_ARGS = re.compile(r"\w+\((.+)\)")


    def search(self, expr):
        match = self.value.search(expr)
        # print("->", expr, ":", match.group(1))
        if match:
            return match.group(1)
        else:
            raise SyntaxError()