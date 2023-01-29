import re
from dataclasses import dataclass, field
from types import FunctionType as function



@dataclass
class Variable:
    value: any
    const: bool


@dataclass
class Function:
    name: str
    args: list[str]
    fn_def: int | function

    @property
    def is_default(self):
        return not isinstance(self.fn_def, int)


@dataclass
class Error(Exception):
    msg: str = ""

    def traceback(self, exe):
        return f">> {exe.file} (line {exe.pc + 1})\n   '{exe.curr_line.strip()}'"    

    def __call__(self, msg, exe):
        self.msg = msg
        return self
    


@dataclass
class Regex:

    expressions: dict[str, str] = field(default_factory=lambda:{
        'set': r"^set\s+(\w+)",
        'let': r"^let\s+(\w+)",
        'const': r"^const\s+(\w+)",
        'reassign': r"^(\w+)\s*=\s*(\w+)",
        'fn_call': r"^([a-zA-Z_][a-zA-Z0-9_]*)\(([^)]*)\)",
        'fn_def': r"^fn\s+(\w+)\((.*)\)",
        'for': r"^for\s+(\w+)\s+from\s+([-]?\d+)\s+to\s+([-]?\d+)(\s+step\s+([-]?\d+))?",
        'expr': r"=\s*(.*)",
        'split': r"(\".*?\"|'.*?'|[^\s]+)",
      
    })

    def __post_init__(self):
        self.expressions = {key: re.compile(value) for key, value in self.expressions.items()}

    @classmethod
    def is_string(self, value):
        return bool(re.search(r"^'[^']*'$", value))


    # FOR = Pattern(re.compile(r"for\s+(.*)"), for_)
    # IF = Pattern(re.compile(r"if\s+(.*)"), if_)
    # ELSE = Pattern(re.compile(r"else\s+(.*)"), else_)
    # WHILE = Pattern(re.compile(r"while\s+(.*)"), while_)
    # BREAK = Pattern(re.compile(r"break\s+(.*)"), break_)
    # CONTINUE = Pattern(re.compile(r"continue\s+(.*)"), continue_)
    # RETURN = Pattern(re.compile(r"ret\s+(.*)"), return_)

