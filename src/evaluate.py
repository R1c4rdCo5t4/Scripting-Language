import ast
import operator as op
from classes import *


def check_undefined_vars(tree, vars):
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id not in vars:
            return node.id

    return None


def evaluate(expr, vars):

    operations = { 
        ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
        ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
        ast.Mod: op.mod, ast.USub: op.neg, ast.FloorDiv: op.floordiv 
    }

    node = ast.parse(expr, mode='eval')
    if undefined := check_undefined_vars(node, vars):
        raise Error(f"undefined variable '{undefined}'")

    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        
        elif isinstance(node, ast.Str):
            return node.s
        
        elif isinstance(node, ast.BinOp):
            if isinstance(node.left, ast.Str) or isinstance(node.right, ast.Str):
                return str(_eval(node.left)) + str(_eval(node.right))
            
            else:
                return operations[type(node.op)](_eval(node.left), _eval(node.right))
            
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return operations[ast.USub](_eval(node.operand))
        
        elif isinstance(node, ast.IfExp):
            return _eval(node.body) if _eval(node.test) else _eval(node.orelse)
        
        else:
            raise Error(f"invalid syntax: '{expr}'")

    return _eval(node.body)
