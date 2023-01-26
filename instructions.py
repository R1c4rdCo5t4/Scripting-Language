import re


reserved_keywords = {"print", "set", "let", "for", "from", "to"}

def validate_var_name(var):
    return bool(re.search(r"^[a-zA-Z_][a-zA-Z0-9_]*$", var))

def assign(exe, var, expr):
    exe.vars[var] = eval(str(expr))


def assign_(exe, re):
    regex = re.ASSIGN.value.pattern.search(exe.curr_line)
    var = regex.group(1)
    val = regex.group(2)
    expr = exe.convert_expr(val)
    assign(exe, var, expr)
    

def set_(exe, re):
    var = re.SET.search(exe.curr_line)

    if not validate_var_name(var):
        raise SyntaxError(f"'{var}' is an invalid variable name")
                
    if var in reserved_keywords:
        raise SyntaxError(f"'{var}' is a reserved keyword")
    
  

    regex = re.EXPR.search(exe.curr_line)
    expr = exe.convert_expr(regex)
    
    assign(exe, var, expr)

    
def let_(exe, re):
    var = re.LET.search(exe.curr_line)
    assign(exe, var, None)


def print_(exe, re):
    regex = re.FUNC_ARGS.search(exe.curr_line)
    expr = exe.convert_expr(regex)
    print(eval(expr))


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


