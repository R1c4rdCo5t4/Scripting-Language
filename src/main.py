import sys
import getopt
import traceback
from execution import *



def main():
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hf:', ['help', 'file'])
        file = None

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                print('main.py -f <file>')
                return
            elif opt in ('-f', '--file'):
                file = arg
    except getopt.GetoptError as e:
        print(e.msg)
        return
    
    exe = Execution(file)

    while exe.running:
        try:
            exe.execute() # line by line
        
        except KeyboardInterrupt:
            break
       
        except Exception as e:
            print(exe.curr_line)
            raise e
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

