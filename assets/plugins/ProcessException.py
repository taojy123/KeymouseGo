class ProcessException(Exception):
    def __init__(self, *args):
        self.args = args


# 跳转到索引为index的脚本行
class JumpProcess(ProcessException):
    def __init__(self, index: int):
        self.index = index


# 当前状态压栈，执行新脚本
class PushProcess(ProcessException):
    def __init__(self, scriptpath: str, extension: str = 'Extension', runtimes: int = 1, speed: int = 100):
        self.scriptpath = scriptpath
        self.extension = extension
        self.runtimes = runtimes
        self.speed = speed


# 执行返回的事件
class AdditionProcess(ProcessException):
    def __init__(self, events):
        self.events = events


# 终止当前执行
class BreakProcess(ProcessException):
    def __init__(self):
        pass


# 终止全部执行
class EndProcess(ProcessException):
    def __init__(self):
        pass
