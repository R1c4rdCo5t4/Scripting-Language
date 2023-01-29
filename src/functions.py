from evaluate import *
from classes import *


def print_(*values):
    values = " ".join(*values)
    print(values)


default_functions = {
    'print': Function('print_', ['value'], print)
}