import sys
import traceback
from execution import *

def main():
    file = sys.argv[1]
    exe = Execution(file)

    # try:
    while not exe.eof:
        exe.execute() # line by line

    # except Exception as e:
        
    #     tb = traceback.extract_tb(e.__traceback__)
    #     print(f'Error in {tb[-1].filename}, line {tb[-1].lineno}')

    #     if hasattr(e, 'traceback'):
    #         print(e.traceback(exe))
      
    #     print(e)
        

        
       

if __name__ == "__main__":
    main()

        

