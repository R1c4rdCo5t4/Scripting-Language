from execution import *
import sys

file = sys.argv[1]
exe = Execution(file)

while not exe.eof:
    exe.execute() # line by line

   

        

