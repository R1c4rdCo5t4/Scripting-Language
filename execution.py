import re
from dataclasses import dataclass, field
from regex import Regex



@dataclass
class Execution:
    file: str
    lines: list[str] = field(default_factory=list)
    pc : int = 0
    ops : str = '+-*/^'
    vars: dict[str, str] = field(default_factory=lambda: {
        '/': '//',
        '^': '**'
    })
    
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
        return len(self.curr_line) == 0 or self.curr_line[0] == '#' or self.curr_line.strip() == ''
    

    def substitute(self, match):
        var = match.group(1)
        if var in self.vars.keys():
            val = self.vars[var]
            return f"'{val}'" if (isinstance(val, str)) else str(val)
        
        return var


    def convert_expr(self, expr: list[str]) -> str:
  
        expr = re.sub(r"\b(\w+)\b", self.substitute, expr)
        if '?' in expr and ':' in expr:
            expr = self.convert_ternary(expr)

        return expr


    def execute(self):

    
        if(self.ignore_line):
            self.pc += 1
            return
        
        for r in list(Regex):
            match = r.value.pattern.search(self.curr_line.strip())
            if match:
                if callback := r.value.callback:
                    callback(self, Regex)
                    break

        self.pc += 1
            

    






    # def is_string(self, value):
    #     return bool(re.search(r"^'[^']*'$", value))

    # def convert_ternary(self, expr):    
    #     split = expr.split(' ? ')
      
    #     cond = split[0]
    #     out = split[1].split(' : ')
    #     true = out[0]
    #     false = out[1]
    #     print(f"{true} if {cond} else {false}")
    #     return f"{true} if {cond} else {false}"