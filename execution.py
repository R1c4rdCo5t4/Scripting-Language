from importlib import import_module
from dataclasses import dataclass, field
from classes import *
from functions import default_functions


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
    vars: dict[str, any] = field(default_factory=default_ops)
    functions: dict[str, Function] = field(default_factory=lambda: default_functions)
    regex: Regex = field(default_factory=Regex)

    
    def __post_init__(self):
        with open(self.file, "r") as f:
            self.lines = f.read().splitlines()


    @property
    def curr_line(self):
        return self.lines[self.pc]
    
    @property
    def eof(self):
        return self.pc >= len(self.lines)
    
    @property
    def ignore_line(self):
        return self.curr_line.strip() == '' or self.curr_line[0] == '#'
    

    def assign_var(self, name, value, const=False):
        self.vars[name] = Variable(value, const)
    

    def convert_ternary(self, expr):    
        cond, true, false = expr.replace(' ? ', ':').split(':')
        return f"{true} if {cond} else {false}"
   

    def substitute_symbols(self, expr):
        for key, value in self.vars.items():
            expr = expr.replace(key, str(value.value) if isinstance(value, Variable) else value)

        return expr


    def convert_expr(self, expr: list[str]) -> str:
  
        expr = self.substitute_symbols(expr)

        if '?' in expr and ':' in expr:
            expr = self.convert_ternary(expr)


        return expr


    def search_line_expr(self, expr, start=1, end=1, all=False):
        match = self.regex.expressions[expr].search(self.curr_line.strip())

        if not match:
            raise Error(f"invalid syntax: '{self.curr_line}'")

        return match.groups() if all else match.group(start) if start == end else match.group(start, end)
    

    def execute(self):

        if self.curr_line.count('###') == 1: # multi-line comment
            self.pc += 1
            while self.curr_line.count('###') != 1 and not self.eof:
                self.pc += 1
        
    
        if self.ignore_line: # empty line or comment
            self.pc += 1
            return
    

      
        for name, regex in self.regex.expressions.items():
        
            match = regex.search(self.curr_line.strip())
            items = match.groups() if match else None
           
            if match:
                inst_name = name + '_'
                

                if name == 'fn_call':
                    if items[0] in self.functions.keys():
                        fn_call = getattr(inst_module, 'fn_call_')
                        fn_call(self)
                    else:
                        raise Error(f"invalid syntax: undefined function '{items[0]}'")
                
                elif inst := getattr(inst_module, inst_name, None):
                    inst(self)
                    

                    

                else:
                    raise Error(f"invalid syntax: '{inst_name[:-1]}'")
                
                break

        else:
            raise Error(f"invalid syntax: unknown instruction")
        
        self.pc += 1
            

    






# def is_string(self, value):
#     return bool(re.search(r"^'[^']*'$", value))

