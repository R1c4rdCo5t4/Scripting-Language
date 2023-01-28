import re
from evaluate import *
from classes import *
from importlib import import_module


fn_module = import_module('functions')
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



""" INSTRUCTIONS """

def reassign_(exe):
    var, val = exe.search_line_expr('reassign', 1, 2)
    expr = exe.convert_expr(val)

    if var not in list(map(lambda x: x.lower(), exe.vars.keys())):
        raise Error(f"undefined variable '{var}'")
    
    if exe.vars[var].const:
        raise Error(f"cannot reassign value to constant '{var}'")
                        
    _assign_var(exe, var, expr)
    

def set_(exe):
    var = exe.search_line_expr('set')
    _validate_var_name(var, exe.vars.keys())
    match = exe.search_line_expr('expr')
    expr = exe.convert_expr(match)
    _assign_var(exe, var, expr)
    

def let_(exe):
    var = exe.search_line_expr('let')
    _validate_var_name(var, exe.vars.keys())
    _assign_var(exe, var)


def const_(exe):
    var = exe.search_line_expr('const')
    regex = exe.search_line_expr('expr')
    expr = exe.convert_expr(regex)
    _assign_var(exe, var, expr, True)





def for_(exe):
    var, start, end, *step = exe.search_line_expr('for', all=True)
    step = int(step[1]) if step[1] else 1
    start, end = int(start), int(end) + 1
    ref = exe.pc
    ident_size = 0
    temp_vars = set()
    
    for i in range(start, end, step):
        _assign_var(exe, var, i)
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



def fn_call_(exe):

    fn_name, args = exe.search_line_expr('fn_call', all=True)
    args = args.split(',')
    fn = exe.functions[fn_name]
    if len(args) != len(fn.args):
        raise Error(f"function error: invalid number of arguments for function '{fn_name}' (expected {len(fn.args)}, got {len(args)}))")
    


    expr = [exe.convert_expr(arg) for arg in args]
    eval_args = [str(evaluate(e, exe.vars.keys())) for e in expr]
   
    if fn.default:
        fn_call = getattr(fn_module, fn_name + '_')
        fn_call(eval_args)


    else:
        for i, arg in enumerate(args):
            _assign_var(exe, fn.args[i], arg)
        
        exe.pc = fn.line
        exe.execute()
        exe.pc = fn.line + fn.size + 1
        for arg in fn.args:
            del exe.vars[arg]