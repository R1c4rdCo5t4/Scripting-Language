import re

from dataclasses import dataclass
from enum import Enum
from instructions import *

@dataclass
class Pattern():
    pattern: re.Pattern
    callback: callable = None


class Regex(Enum):
    SET = Pattern(re.compile(r"set\s+(\w+)"), set_)
    LET = Pattern(re.compile(r"let\s+(\w+)"), let_)
    ASSIGN = Pattern(re.compile(r"(\w+)\s*=\s*(\w+)"), assign_)
    FUNC_ARGS = Pattern(re.compile(r"\w+((.+))"))
    EXPR = Pattern(re.compile(r"=\s*(.*)"))
    PRINT = Pattern(re.compile(r"^print(.*)"), print_)
    
    # FOR = Pattern(re.compile(r"for\s+(.*)"), for_)
    # IF = Pattern(re.compile(r"if\s+(.*)"), if_)
    # ELSE = Pattern(re.compile(r"else\s+(.*)"), else_)
    # WHILE = Pattern(re.compile(r"while\s+(.*)"), while_)
    # BREAK = Pattern(re.compile(r"break\s+(.*)"), break_)
    # CONTINUE = Pattern(re.compile(r"continue\s+(.*)"), continue_)
    # RETURN = Pattern(re.compile(r"ret\s+(.*)"), return_)

    def search(self, pattern):
        match = self.value.pattern.search(pattern)
        if match:
            return match.group(1)

        raise SyntaxError()


