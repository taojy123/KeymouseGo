from platform import system
from PySide2.QtCore import Slot
import Recorder.globals

if system() == 'Windows':
    import Recorder.WindowsRecorder as _Recoder
elif system() in ['Linux', 'Darwin']:
    pass
else:
    raise OSError("Unsupported platform '{}'".format(system()))

_Recoder.setuphook()
Recorder = _Recoder


# 捕获到事件后调用函数
def set_callback(callback):
    _Recoder.record_signals.event_signal.connect(callback)


# 槽函数:改变鼠标精度
@Slot(int)
def set_interval(value):
    globals.mouse_interval_ms = value
