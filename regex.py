import re
from enum import Enum


class Regex(Enum):
    VAR_NAME = (re.compile(r"(set|let)\s+(\w+)"), 2)
    RIGHT_SIDE = (re.compile(r"\s*=\s*(.+)"), 1)
    FUNC_ARGS = (re.compile(r"\w+<(.+)>"), 1)

    def search(self, expr):
        match = self.value[0].search(expr)
        if match:
            return match.group(self.value[1])
        else:
            raise SyntaxError()