import re
from dataclasses import dataclass, field
from regex import Regex


reserved_keywords = {"print", "set", "for", "from", "to"}


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
        
        split = list(filter(lambda x: x != '', re.split("[\s()]", self.curr_line.strip())))

        match(split[0]):
            case 'set':
                
                var = Regex.VAR_NAME.search(self.curr_line)
                
                if var in reserved_keywords:
                    raise SyntaxError()

                regex = Regex.RIGHT_SIDE.search(self.curr_line)
                expr = self.convert_expr(regex)
                self.vars[var] = eval(str(expr))

            case 'print':
                regex = Regex.FUNC_ARGS.search(self.curr_line)
                expr = self.convert_expr(regex)
                print(eval(expr))


            case 'for':
                var = split[1]
                start = int(split[3])
                end = int(split[5].strip(':')) + 1
                step = 1 if len(split) < 7 else int(split[7].strip(':'))
            
                ref = self.pc
                temp_vars = set()
                for i in range(start, end, step):
                    
                    self.vars[var] = str(i)
                    temp_vars.add(var)
                    
                    self.pc += 1

                    while self.pc < len(self.lines):
               
                        if len(self.curr_line) > 4 and self.curr_line[:4] == '    ':
                            self.execute()
                        else:
                            self.pc += 1
                        
                        
                    if i != end-step:
                        self.pc = ref
                    
                self.pc += 1
                for v in temp_vars:
                    del self.vars[v]


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