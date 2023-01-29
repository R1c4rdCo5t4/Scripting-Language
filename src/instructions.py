from classes import *
from importlib import import_module
from helpers import *

fn_module = import_module('functions')


def reassign_(exe):
    var, val = exe.search_line_expr('reassign', 1, 2)
    expr = exe.convert_expr(val)

    if var not in list(map(lambda x: x.lower(), exe.vars.keys())):
        raise Error(f"undefined variable '{var}'")
    
    if exe.vars[var].const:
        raise Error(f"cannot reassign value to constant '{var}'")
                        
    assign_var(exe, var, expr)


def set_(exe):
    var = exe.search_line_expr('set')
    validate_var_name(var, exe.vars.keys())
    match = exe.search_line_expr('expr')
    expr = exe.convert_expr(match)
    assign_var(exe, var, expr)
    

def let_(exe):
    var = exe.search_line_expr('let')
    validate_var_name(var, exe.vars.keys())
    assign_var(exe, var)


def const_(exe):
    var = exe.search_line_expr('const')
    regex = exe.search_line_expr('expr')
    expr = exe.convert_expr(regex)
    assign_var(exe, var, expr, True)


def for_(exe):
    var, start, end, *step = exe.search_line_expr('for', all=True)
    step = int(step[1]) if step[1] else 1
    start, end = int(start), int(end) + 1
    ref = exe.pc
    ident_size = 0
    temp_vars = set()
    
    for i in range(start, end, step):
        assign_var(exe, var, i)
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
    args = filter_args(args)
    
    if fn_name not in exe.functions.keys():
        raise Error(f"invalid syntax: undefined function '{fn_name}'")
    
    fn = exe.functions[fn_name]
    if len(args) != len(fn.args):
        raise Error(f"function error: invalid number of arguments for function '{fn_name}' (expected {len(fn.args)}, got {len(args)}))")

    expr = [exe.convert_expr(arg) for arg in args]
    if fn.is_default:
        eval_args = [str(evaluate(e, exe.vars.keys())) for e in expr]
        fn_call = getattr(fn_module, fn_name + '_')
        fn_call(eval_args)

    else:
        for i, arg in enumerate(args):
            print(fn.args[i], exe.substitute_symbols(arg))
            assign_var(exe, fn.args[i], exe.substitute_symbols(arg))
        
        if not isinstance(fn.fn_def, int):
            raise Error(f"function error: invalid reference for function '{fn_name}'")
        
        exe.pc = fn.fn_def
        while not exe.eof and (not exe.curr_line or exe.curr_line[:4] == '    '):
            exe.execute()
            exe.pc += 1
        
        for arg in fn.args:
            del exe.vars[arg]


def fn_def_(exe):
    fn_name, args = exe.search_line_expr('fn_def', all=True)
    args = filter_args(args)
    exe.pc += 1
    ref = exe.pc
    exe.functions[fn_name] = Function(fn_name, args, ref)


