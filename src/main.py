
import sys
import traceback
from execution import *


def main():
    file = sys.argv[1]
    exe = Execution(file)

    while exe.running:
        try:
            exe.execute() # line by line
        
        except KeyboardInterrupt:
            break
       
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            print(f'Error in {tb[-1].filename}, line {tb[-1].lineno}')

            if hasattr(e, 'traceback'):
                print(e.traceback(exe))
        
            print(e)
           
            if not exe.shell_mode:
                break
            
            exe.pc += 1



if __name__ == "__main__":
    main()

