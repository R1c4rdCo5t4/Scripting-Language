import re
from evaluate import *
from errors import Error

reserved_keywords = {"print", "set", "let", "const", "for", "from", "to"}


def _validate_var_name(var, vars):
    if not bool(re.search(r"^[a-zA-Z_][a-zA-Z0-9_]*$", var)):
        raise Error(f"'{var}' is an invalid variable name")
                
    if var in reserved_keywords:
        raise Error(f"'{var}' is a reserved keyword") 
    
    if var in vars:
        raise Error(f"'{var}' is already defined")


def _assign_var(exe, var, expr=None, const=False):
    value = evaluate(str(expr), exe.vars.keys())
    exe.assign_var(var, value, const)


def reassign_(exe, re):
    regex = re.REASSIGN.value.pattern.search(exe.curr_line)
    var = regex.group(1)
    val = regex.group(2)
    expr = exe.convert_expr(val)

    if var not in list(map(lambda x: x.lower(), exe.vars.keys())):
        raise Error(f"undefined variable '{var}'")
    
    if exe.vars[var].const:
        raise Error(f"cannot reassign value to constant '{var}'")
                          
    _assign_var(exe, var, expr)
    

def set_(exe, re):
    var = re.SET.search(exe.curr_line)
    _validate_var_name(var, exe.vars.keys())
    regex = re.EXPR.search(exe.curr_line)
    expr = exe.convert_expr(regex)
    _assign_var(exe, var, expr)
    

def let_(exe, re):
    var = re.LET.search(exe.curr_line)
    _validate_var_name(var, exe.vars.keys())
    _assign_var(exe, var)


def const_(exe, re):
    var = re.CONST.search(exe.curr_line)
    regex = re.EXPR.search(exe.curr_line)
    expr = exe.convert_expr(regex)
    _assign_var(exe, var, expr, True)

    
def print_(exe, re):
    regex = re.FUNC_ARGS.search(exe.curr_line)
    expr = exe.convert_expr(regex)
    value = evaluate(str(expr), exe.vars.keys()) if expr != '(None)' else 'undefined'
    print(value)


def for_(exe, re):

    match = re.FOR.value.pattern.search(exe.curr_line)
    var, start, end, *step = match.groups()
    step = int(step[1]) if step[1] else 1
    start, end = int(start), int(end) + 1

    ref = exe.pc
    ident_size = 0
    temp_vars = set()
    
    for i in range(start, end, step):
        exe.vars[var] = str(i)
        temp_vars.add(var)                    
        exe.pc += 1
        ident_size = 0
        while not exe.eof and (not exe.curr_line or exe.curr_line[:4] == '    '):
            exe.execute()
            ident_size += 1

        exe.pc = ref
        
    exe.pc = ref + ident_size
    for v in temp_vars:
        del exe.vars[v]


