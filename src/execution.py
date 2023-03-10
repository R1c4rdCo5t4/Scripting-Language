from importlib import import_module
from dataclasses import dataclass, field
from classes import *
from functions import default_functions
from helpers import *


inst_module = import_module('instructions')
default_ops = lambda: {
    '/': '//',
    '^': '**',
    'undefined': 'None',
    'null': 'None',
    'true': 'True',
    'false': 'False',
    'isnt': 'is not',
}


@dataclass
class Execution:
    file: str
    lines: list[str] = field(default_factory=list)
    pc : int = 0
    vars: dict[str, any] = field(default_factory=dict)
    ops: dict[str, str] = field(default_factory=default_ops)
    functions: dict[str, Function] = field(default_factory=lambda: default_functions)
    regex: Regex = field(default_factory=Regex)
    
    def __post_init__(self):
        if not self.shell_mode:
            with open(self.file, "r") as f:
                self.lines = f.read().splitlines()
    
    @property
    def shell_mode(self):
        return self.file == None

    @property
    def running(self):
        if self.shell_mode:
            return True
        
        return not self.eof

    @property
    def curr_line(self):
        return self.lines[self.pc]
    
    @property
    def eof(self):
        return self.pc >= len(self.lines)
    
    @property
    def ignore_line(self): # single-line comment or empty lines
        return self.curr_line.strip() == '' or self.curr_line.strip().startswith('#')
    

    @property
    def ignore_lines(self): # multi-line comment
        if self.curr_line.strip().startswith('###'): 
            self.pc += 1
            while self.curr_line.strip().startswith('###') and not self.eof:
                self.pc += 1
            
            return True
        return False
    
    def reset(self):
        self.pc = 0
        self.vars = {}
        self.functions = default_functions
    

    def assign_var(self, name, value, const=False):
        value = evaluate(str(value), self.vars)
        tp = type(value).__name__
        self.vars[name] = Variable(value, tp, const)


    def convert_ternary(self, expr):    
        cond, true, false = expr.replace(' ? ', ' : ').split(' : ')
        return f"{true} if {cond} else {false}"
   

    def substitute_symbols(self, expr):
        parts = re.split(self.regex.expressions['split'], str(expr).strip())
        parts = filter_empty(parts)

        for i, part in enumerate(parts):
            if not Regex.is_string(part):
                if val := self.vars.get(part, None):
                    value = val.value if isinstance(val, Variable) else val
                    parts[i] = f"'{value}'" if isinstance(value, str) else str(value)

        return ''.join(parts)



    def convert_expr(self, expr: list[str]) -> str:
        expr = self.substitute_symbols(expr)
        if '?' in expr and ':' in expr:
            expr = self.convert_ternary(expr)

        return expr


    def search_line_expr(self, expr, start=1, end=1, all=False):
        match = self.regex.patterns[expr].search(self.curr_line.strip())
        if not match:
            raise Error(f"invalid syntax: '{self.curr_line}'")

        return match.groups() if all else match.group(start) if start == end else match.group(start, end)


    def execute(self):

        if self.eof:
            raise Error("interpreter error: end of file reached")

        if self.shell_mode:
            new_line = input('>>> ')
            self.lines.append(new_line)

        if self.ignore_lines or self.ignore_line:       
            self.pc += 1
            return
        
        for name, regex in self.regex.instructions.items():
            if regex.search(self.curr_line.strip()):
                inst_name = name + '_'
                inst = getattr(inst_module, inst_name, None)
                inst(self)
                break
        else:
            raise Error(f"invalid syntax: unknown instruction '{self.curr_line}''")
        
        self.pc += 1