from evaluate import *
from classes import *


def print_(exe, args, *eval_args):
    values = " ".join(*eval_args)
    print(values)


def log_(exe, args, eval_args):
    var = args[0]
    if var not in exe.vars.keys():
        raise Error(f"invalid argument for log function: {var}")
    
    print(f"{var} = {exe.vars[var].value} ({(exe.vars[var]).type.__name__})")


default_functions = {
    'print': Function('print_', ['*'], print),
    'log': Function('log_', ['var'], log_),
}