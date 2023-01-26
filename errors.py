from dataclasses import dataclass

@dataclass
class Error(Exception):
    msg: str = ""

    def message(self, exe):
        return f"file '{exe.file}' (line {exe.pc + 1})\n    '{exe.curr_line.strip()}'\n{self.msg}"    

    def __call__(self, msg, exe):
        self.msg = msg
        return self