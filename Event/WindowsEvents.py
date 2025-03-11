import re
import pyperclip
import win32api

from Event.Event import Event
from loguru import logger

import ctypes
import win32con
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
numofmonitors = user32.GetSystemMetrics(win32con.SM_CMONITORS)
# 主屏分辨率
SW, SH = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


class WindowsEvent(Event):
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

    # 执行操作
    def execute(self, thd=None):
        self.sleep(thd)

        if self.event_type == 'EM':
            x, y = self.action
            # 兼容旧版的绝对坐标
            if not isinstance(x, int) and not isinstance(y, int):
                x = float(re.match('([0-1].[0-9]+)%', x).group(1))
                y = float(re.match('([0-1].[0-9]+)%', y).group(1))

            if self.action == [-1, -1]:
                # 约定 [-1, -1] 表示鼠标保持原位置不动
                pass
            else:
                # 挪动鼠标 普通做法
                # ctypes.windll.user32.SetCursorPos(x, y)
                # or
                # win32api.SetCursorPos([x, y])

                # 更好的兼容 win10 屏幕缩放问题
                if isinstance(x, int) and isinstance(y, int):
                    if numofmonitors > 1:
                        win32api.SetCursorPos([x, y])
                    else:
                        nx = int(x * 65535 / SW)
                        ny = int(y * 65535 / SH)
                        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx, ny, 0, 0)
                else:
                    nx = int(x * 65535)
                    ny = int(y * 65535)
                    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx, ny, 0, 0)

            if self.action_type == 'mouse left down':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            elif self.action_type == 'mouse left up':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif self.action_type == 'mouse right down':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            elif self.action_type == 'mouse right up':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            elif self.action_type == 'mouse middle down':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            elif self.action_type == 'mouse middle up':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            elif self.action_type == 'mouse wheel up':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA, 0)
            elif self.action_type == 'mouse wheel down':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -win32con.WHEEL_DELTA, 0)
            elif self.action_type == 'mouse move':
                pass
            else:
                logger.warning('Unknown mouse event:%s' % self.action_type)

        elif self.event_type == 'EK':
            key_code, key_name, extended = self.action

            # shift ctrl alt
            # if key_code >= 160 and key_code <= 165:
            #     key_code = int(key_code/2) - 64

            # 不执行热键
            # if key_name in HOT_KEYS:
            #     return

            base = 0
            if extended:
                base = win32con.KEYEVENTF_EXTENDEDKEY

            if self.action_type == 'key down':
                win32api.keybd_event(key_code, 0, base, 0)
            elif self.action_type == 'key up':
                win32api.keybd_event(key_code, 0, base | win32con.KEYEVENTF_KEYUP, 0)
            else:
                logger.warning('Unknown keyboard event:', self.action_type)

        elif self.event_type == 'EX':

            if self.action_type == 'input':
                text = self.action
                pyperclip.copy(text)
                # Ctrl+V
                win32api.keybd_event(162, 0, 0, 0)  # ctrl
                win32api.keybd_event(86, 0, 0, 0)  # v
                win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(162, 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                logger.warning('Unknown extra event:%s' % self.action_type)
