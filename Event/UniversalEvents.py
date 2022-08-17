import re

# import pyperclip
import pyautogui
from Event.Event import Event
from loguru import logger

SW, SH = pyautogui.size()


class UniversalEvent(Event):
    # 改变坐标
    # pos 为包含横纵坐标的元组
    # 值为int型:绝对坐标
    # 值为float型:相对坐标
    def changepos(self, pos: tuple):
        if self.event_type == 'EM':
            x, y = pos
            if isinstance(x, int):
                self.action[0] = x
            else:
                self.action[0] = int(x * SW)
            if isinstance(y, int):
                self.action[1] = y
            else:
                self.action[1] = int(y * SH)

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
                if not isinstance(x, int):
                    x = int(x * SW)
                if not isinstance(y, int):
                    y = int(y * SH)
                pyautogui.moveTo(x, y)

            if self.message == 'mouse left down':
                pyautogui.mouseDown(button='left')
            elif self.message == 'mouse left up':
                pyautogui.mouseUp(button='left')
            elif self.message == 'mouse right down':
                pyautogui.mouseDown(button='right')
            elif self.message == 'mouse right up':
                pyautogui.mouseUp(button='right')
            elif self.message == 'mouse middle down':
                pyautogui.mouseDown(button='middle')
            elif self.message == 'mouse middle up':
                pyautogui.mouseUp(button='middle')
            elif self.message == 'mouse wheel up':
                pyautogui.scroll(1)
            elif self.message == 'mouse wheel down':
                pyautogui.scroll(-1)
            elif self.message == 'mouse move':
                pass
            else:
                logger.warning('Unknown mouse event:%s' % self.message)

        elif self.event_type == 'EK':
            key_code, key_name, extended = self.action

            if self.message == 'key down':
                pyautogui.keyDown(key_name)
            elif self.message == 'key up':
                pyautogui.keyUp(key_name)
            else:
                logger.warning('Unknown keyboard event:', self.message)

        elif self.event_type == 'EX':
            if self.message == 'input':
                text = self.action
                # pyperclip.copy(text)

                pyautogui.write(text)
                # Ctrl+V
                # keyboardctl.press('ctrl')
                # keyboardctl.press('v')
                # keyboardctl.release('v')
                # keyboardctl.release('ctrl')
            else:
                logger.warning('Unknown extra event:%s' % self.message)

