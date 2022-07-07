import time

from Event import ScriptEvent
from PySide2.QtCore import Signal, QObject
from winreg import QueryValueEx, OpenKey, HKEY_CURRENT_USER, KEY_READ
# 是否切换主要/次要功能键
swapmousebuttons = True if QueryValueEx(OpenKey(HKEY_CURRENT_USER,
                                                r'Control Panel\Mouse',
                                                0,
                                                KEY_READ),
                                        'SwapMouseButtons')[0] == '1' else False
swapmousemap = {'mouse left down': 'mouse right down', 'mouse left up': 'mouse right up',
                'mouse right down': 'mouse left down', 'mouse right up': 'mouse left up'}

latest_time = -1
mouse_interval_ms = 200


def current_ts():
    return int(time.time() * 1000)


class RecordSignal(QObject):
    event_signal = Signal(ScriptEvent)
