import re
from dataclasses import dataclass, field

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
        return len(self.lines[self.pc]) == 0 or self.lines[self.pc][0] == '#'


    def evaluate(self, expr: list[str]) -> int:
        expr = "".join([x.replace(x, self.vars[x]) if x in self.vars.keys() else x for x in expr])
        return eval(expr)


    def execute(self):
        if(self.ignore_line):
            self.pc += 1
            return
        
        split = list(filter(lambda x: x != '', re.split("[\s()]", self.lines[self.pc].strip())))

        match(split[0]):
            case 'set':
                var = split[1]
                expr = split[3:]
                self.vars[var] = str(self.evaluate(expr))

            case 'print':
                expr = [str(x) for x in split[1:]]
                print(self.evaluate(expr))

            case 'for':
                var = split[1]
                start = int(split[3])
                end = int(split[5].strip(':')) + 1
                step = 1 if len(split) < 7 else int(split[7].strip(':'))
            
                ref = self.pc
                for i in range(start, end, step):
                    self.vars[var] = str(i)
                    self.pc += 1

                    while(self.pc < len(self.lines) and len(self.lines[self.pc]) > 4 and self.lines[self.pc][:4] == '    '):
                        self.execute()
                        self.pc += 1
                        
                    if i != end-step:
                        self.pc = ref
                    
                self.pc += 1

        self.pc += 1
            