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
                        
    exe.assign_var(var, expr)


def set_(exe):
    var = exe.search_line_expr('set')
    validate_var_name(var, exe.vars.keys())
    match = exe.search_line_expr('expr')
    expr = exe.convert_expr(match)
    exe.assign_var(var, expr)
    

def let_(exe):
    var = exe.search_line_expr('let')
    validate_var_name(var, exe.vars.keys())
    exe.assign_var(var, None)


def const_(exe):
    var = exe.search_line_expr('const')
    regex = exe.search_line_expr('expr')
    expr = exe.convert_expr(regex)
    exe.assign_var(var, expr, True)


def for_(exe):
    var, start, end, *step = exe.search_line_expr('for', all=True)
    step = step[1] if step[1] else 1
    start, end, step = list(map(lambda x: int(exe.substitute_symbols(x).strip("'")), [start, end, step]))
    ref = exe.pc
    ident_size = 0
    temp_vars = set()
    
    for i in range(start, end+1, step):
        exe.assign_var(var, i)
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
    if fn.args[0] != '*' and len(args) != len(fn.args):
        raise Error(f"function error: invalid number of arguments for function '{fn_name}' (expected {len(fn.args)}, got {len(args)}))")

    
    expr = [exe.convert_expr(arg) for arg in args]
    if fn.is_default:
        eval_args = [str(evaluate(e, exe.vars.keys())) for e in expr]
        fn_call = getattr(fn_module, fn_name + '_')
        fn_call(exe, args, eval_args)

    else:
        for i, arg in enumerate(args):
            exe.assign_var(fn.args[i], exe.substitute_symbols(arg))
        
        if not isinstance(fn.fn_def, int):
            raise Error(f"function error: invalid reference for function '{fn_name}'")
        
        exe.pc = fn.fn_def
        while not exe.eof and (not exe.curr_line or exe.curr_line[:4] == '    '):
            exe.execute()
            exe.pc += 1
        
        exe.pc += 1
        for arg in fn.args:
            del exe.vars[arg]


def fn_def_(exe):
    fn_name, args = exe.search_line_expr('fn_def', all=True)
    args = filter_args(args)

    if fn_name in exe.functions.keys():
        raise Error(f"function error: function '{fn_name}' is already defined")
    
    if fn_name in reserved_keywords:
        raise Error(f"function error: '{fn_name}' is a reserved keyword")

    if any([arg in reserved_keywords for arg in args]):
        raise Error(f"function error: function arguments cannot be reserved keywords")

    exe.pc += 1
    ref = exe.pc
    exe.functions[fn_name] = Function(fn_name, args, ref)


