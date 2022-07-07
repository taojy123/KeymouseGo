import re
import time

import pyperclip
import win32api
import win32con

from Event.Event import Event, SW, SH
from loguru import logger


class WindowsEvent(Event):
    def summarystr(self):
        if self.event_type == 'EK':
            return 'key {0} {1} after {1}ms'.format(self.action[1], self.message[4:], self.delay)
        else:
            return '{0} after {1}ms'.format(self.message, self.delay)

    # 延时
    def sleep(self, thd=None):
        if thd:
            thd.exe_event.clear()
            thd.exe_event.wait(timeout=self.delay / 1000.0)
            thd.exe_event.set()
        else:
            time.sleep(self.delay / 1000.0)

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
                    nx = int(x * 65535 / SW)
                    ny = int(y * 65535 / SH)
                else:
                    nx = int(x * 65535)
                    ny = int(y * 65535)
                win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx, ny, 0, 0)

            if self.message == 'mouse left down':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            elif self.message == 'mouse left up':
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            elif self.message == 'mouse right down':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            elif self.message == 'mouse right up':
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
            elif self.message == 'mouse middle down':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
            elif self.message == 'mouse middle up':
                win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
            elif self.message == 'mouse wheel up':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA, 0)
            elif self.message == 'mouse wheel down':
                win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -win32con.WHEEL_DELTA, 0)
            elif self.message == 'mouse move':
                pass
            else:
                logger.warning('Unknown mouse event:%s' % self.message)

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

            if self.message == 'key down':
                win32api.keybd_event(key_code, 0, base, 0)
            elif self.message == 'key up':
                win32api.keybd_event(key_code, 0, base | win32con.KEYEVENTF_KEYUP, 0)
            else:
                logger.warning('Unknown keyboard event:', self.message)

        elif self.event_type == 'EX':

            if self.message == 'input':
                text = self.action
                pyperclip.copy(text)
                # Ctrl+V
                win32api.keybd_event(162, 0, 0, 0)  # ctrl
                win32api.keybd_event(86, 0, 0, 0)  # v
                win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(162, 0, win32con.KEYEVENTF_KEYUP, 0)
            else:
                logger.warning('Unknown extra event:%s' % self.message)
