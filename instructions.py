import re
from dataclasses import dataclass, field
from execution import Execution
from regex import Regex


reserved_keywords = {"print", "set", "for", "from", "to"}



def assign_(exe, var, expr):
    exe.vars[var] = eval(str(expr))


def set_(exe: Execution):
    var = Regex.VAR_NAME.search(exe.curr_line)
                
    if var in reserved_keywords:
        raise SyntaxError()

    regex = Regex.RIGHT_SIDE.search(exe.curr_line)
    expr = exe.convert_expr(regex)
    
    assign_(exe, var, expr)

    
def let_(exe: Execution):
    var = Regex.VAR_NAME.search(exe.curr_line)
    assign_(exe, var, None)


def print_(exe: Execution):
    regex = Regex.FUNC_ARGS.search(exe.curr_line)
    expr = exe.convert_expr(regex)
    print(eval(expr))


def for_(exe: Execution):
    pass


    # var = split[1]
    # start = int(split[3])
    # end = int(split[5].strip(':')) + 1
    # step = 1 if len(split) < 7 else int(split[7].strip(':'))

    # ref = exe.pc
    # temp_vars = set()
    
    # for i in range(start, end, step):
        
    #     exe.vars[var] = str(i)
    #     temp_vars.add(var)                    
    #     exe.pc += 1

    #     while not exe.curr_line or exe.curr_line[:4] == '    ':
    #         exe.execute()

    #     if i != end-step:
    #         exe.pc = ref
    
    # exe.pc -= 1
    # for v in temp_vars:
    #     del exe.vars[v]


