from abc import ABCMeta, abstractmethod

import win32con
from win32gui import GetDC
from win32print import GetDeviceCaps

hDC = GetDC(0)
SW = GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
SH = GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)


class Event(metaclass=ABCMeta):
    # 传入字典进行初始化
    def __init__(self, content):
        self.delay = content['delay']
        self.event_type = content['event_type']
        self.message = content['message']
        self.action = content['action']
        self.addon = content.get('addon')

    def __str__(self):
        if self.addon:
            return '[%d, %s, %s, %s, %s]' % (self.delay, self.event_type, self.message, self.action, str(self.addon))
        return '[%d, %s, %s, %s]' % (self.delay, self.event_type, self.message, self.action)

    # 改变坐标
    # pos 为包含横纵坐标的元组
    # 值为int型:绝对坐标
    # 值为float型:相对坐标
    def changepos(self, pos: tuple):
        if self.event_type == 'EM':
            x, y = pos
            if isinstance(x, int):
                self.action[0] = int(x * 65535 / SW)
            else:
                self.action[0] = int(x * 65535)
            if isinstance(y, int):
                self.action[1] = int(y * 65535 / SH)
            else:
                self.action[1] = int(y * 65535)

    @abstractmethod
    def execute(self, thd=None):
        pass
