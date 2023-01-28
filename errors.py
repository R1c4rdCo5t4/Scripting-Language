from dataclasses import dataclass

@dataclass
class Error(Exception):
    msg: str = ""

    def traceback(self, exe):
        return f">> {exe.file} (line {exe.pc + 1})\n   '{exe.curr_line.strip()}'"    

    def __call__(self, msg, exe):
        self.msg = msg
        return self