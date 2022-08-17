class ProcessException(Exception):
    def __init__(self, *args):
        self.args = args


# 跳转到索引为index的脚本行
class JumpProcess(ProcessException):
    def __init__(self, index):
        self.index = index


# 终止当前执行
class BreakProcess(ProcessException):
    def __init__(self):
        pass


# 终止全部执行
class EndProcess(ProcessException):
    def __init__(self):
        pass
