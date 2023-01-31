import re
from classes import Error
from evaluate import *

reserved_keywords = {"print", "set", "let", "const", "for", "from", "to", "fn"}

def filter_values(iterable: list, condition: callable) -> list:
    return list(filter(condition, iterable))

def filter_empty(iterable: list) -> list:
    return filter_values(iterable, lambda x: x != '')

def filter_args(args: list) -> list:
    return filter_empty(args.split(','))

def validate_var_name(var, vars):
    if not bool(re.search(r"^[a-zA-Z_][a-zA-Z0-9_]*$", var)):
        raise Error(f"'{var}' is an invalid variable name")
                
    if var in reserved_keywords:
        raise Error(f"'{var}' is a reserved keyword") 
    
    if var in vars:
        raise Error(f"'{var}' is already defined")


def get_type(value):
    if value == 'None':
        return None
    elif value == 'true' or value == 'false':
        return bool
    elif value[0] == "'" and value[-1] == "'":
        return str
    else:
        return int