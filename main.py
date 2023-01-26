from execution import *
import sys

def main():
    file = sys.argv[1]
    exe = Execution(file)

    while not exe.eof:
        exe.execute() # line by line


if __name__ == "__main__":
    main()

        

