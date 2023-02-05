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

def len_(exe, args, eval_args):
    print(len(args[0]))

def avg_(exe, args, eval_args):
    print(sum(args[0]) / len(args[0]))

def sum_(exe, args, eval_args):
    print(sum(args[0]))

def min_(exe, args, eval_args):
    print(min(args[0]))

def max_(exe, args, eval_args):
    print(max(args[0]))

def abs_(exe, args, eval_args):
    print(abs(args[0]))



default_functions = {
    'print': Function('print_', ['*'], print),
    'log': Function('log_', ['var'], log_),
    'len': Function('len_', ['list'], len_),
    'avg': Function('avg_', ['list'], avg_),
    'sum': Function('sum_', ['list'], sum_),
    'min': Function('min_', ['list'], min_),
    'max': Function('max_', ['list'], max_),
    'abs': Function('abs_', ['num'], abs_),
}