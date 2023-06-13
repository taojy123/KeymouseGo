from platform import system
from PySide6.QtCore import Slot
import Recorder.globals

if system() == 'Windows':
    import Recorder.WindowsRecorder as _Recorder
elif system() in ['Linux', 'Darwin']:
    import Recorder.UniversalRecorder as _Recorder
else:
    raise OSError("Unsupported platform '{}'".format(system()))

setuphook = _Recorder.setuphook


# 捕获到事件后调用函数
def set_callback(callback):
    _Recorder.record_signals.event_signal.connect(callback)


# 槽函数:改变鼠标精度
@Slot(int)
def set_interval(value):
    globals.mouse_interval_ms = value
