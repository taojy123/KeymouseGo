class ProcessException(Exception):
    def __init__(self, *args):
        self.args = args


# 跳轉到索引為index的腳本行
class JumpProcess(ProcessException):
    def __init__(self, index):
        self.index = index


# 終止當前執行
class BreakProcess(ProcessException):
    def __init__(self):
        pass


# 終止全部執行
class EndProcess(ProcessException):
    def __init__(self):
        pass
