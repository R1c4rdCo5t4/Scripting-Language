from evaluate import *
from dataclasses import dataclass, field
from classes import *


def print_(*values):
    values = " ".join(*values)
    print(values)


default_functions = {
    'print': Function('print_', print, ['value'], True)
    
}