# -*- encoding:utf-8 -*-
import collections
import datetime
import json
import os
import re
import sys
import threading
import time
import traceback
import winreg

import pyWinhook
import pyperclip
import win32api
import win32con
import win32gui
import win32print
from PySide2 import QtCore
from PySide2.QtCore import QTranslator, QCoreApplication
from PySide2.QtWidgets import QMainWindow, QApplication
from playsound import playsound, PlaysoundException
from pyWinhook import cpyHook, HookConstants

from UIView import Ui_UIView

HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
            'XButton1', 'XButton2', 'Middle']
hDC = win32gui.GetDC(0)
SW = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
SH = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)

# 是否切换主要/次要功能键
swapmousebuttons = True if winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                              r'Control Panel\Mouse',
                                                              0,
                                                              winreg.KEY_READ),
                                               'SwapMouseButtons')[0] == '1' else False
swapmousemap = {'mouse left down': 'mouse right down', 'mouse left up': 'mouse right up',
                'mouse right down': 'mouse left down', 'mouse right up': 'mouse left up'}


def current_ts():
    return int(time.time() * 1000)


def get_assets_path(*paths):
    # pyinstaller -F --add-data ./assets;assets KeymouseGo.py
    try:
        root = sys._MEIPASS
    except:
        root = os.getcwd()
    return os.path.join(root, 'assets', *paths)


class UIFunc(QMainWindow, Ui_UIView):
    def __init__(self):
        super(UIFunc, self).__init__()

        print('assets root:', get_assets_path())

        self.setupUi(self)

        self.config = self.loadconfig()

        self.setFocusPolicy(QtCore.Qt.NoFocus)

        self.trans = QTranslator(self)
        self.choice_language.addItems(['简体中文', 'English'])
        self.choice_language.currentTextChanged.connect(self.onchangelang)
        self.choice_language.setCurrentText(self.config.value("Config/Language"))
        self.onchangelang()

        if not os.path.exists('scripts'):
            os.mkdir('scripts')
        self.scripts = os.listdir('scripts')[::-1]
        self.scripts = list(filter(lambda s: s.endswith('.txt'), self.scripts))
        self.choice_script.addItems(self.scripts)
        if self.scripts:
            self.choice_script.setCurrentIndex(0)

        self.choice_start.addItems(HOT_KEYS)
        self.choice_stop.addItems(HOT_KEYS)
        self.choice_record.addItems(HOT_KEYS)
        self.choice_start.setCurrentIndex(int(self.config.value("Config/StartHotKeyIndex")))
        self.choice_stop.setCurrentIndex(int(self.config.value("Config/StopHotKeyIndex")))
        self.choice_record.setCurrentIndex(int(self.config.value("Config/RecordHotKeyIndex")))
        self.stimes.setValue(int(self.config.value("Config/LoopTimes")))
        self.mouse_move_interval_ms.setValue(int(self.config.value("Config/Precision")))
        self.execute_speed.setValue(int(self.config.value("Config/ExecuteSpeed")))
        self.choice_start.currentIndexChanged.connect(self.onconfigchange)
        self.choice_stop.currentIndexChanged.connect(self.onconfigchange)
        self.choice_record.currentIndexChanged.connect(self.onconfigchange)
        self.stimes.valueChanged.connect(self.onconfigchange)
        self.execute_speed.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(self.onconfigchange)

        self.running = False
        self.recording = False
        self.record = []
        self.ttt = current_ts()

        # for pause-resume feature
        self.paused = False
        self.pause_event = threading.Event()

        # Pause-Resume Record
        self.pauserecord = False

        self.actioncount = 0

        # For better thread control
        self.runthread = None
        self.isbrokenorfinish = True

        self.btrun.clicked.connect(self.OnBtrunButton)
        self.btrecord.clicked.connect(self.OnBtrecordButton)
        self.btpauserecord.clicked.connect(self.OnPauseRecordButton)
        self.choice_record.installEventFilter(self)
        self.choice_language.installEventFilter(self)
        self.choice_stop.installEventFilter(self)
        self.choice_script.installEventFilter(self)
        self.choice_start.installEventFilter(self)
        self.btrun.installEventFilter(self)
        self.btrecord.installEventFilter(self)
        self.btpauserecord.installEventFilter(self)

        self.hm = pyWinhook.HookManager()

        def on_mouse_event(event):

            # print('MessageName:',event.MessageName)  #事件名称
            # print('Message:',event.Message)          #windows消息常量
            # print('Time:',event.Time)                #事件发生的时间戳
            # print('Window:',event.Window)            #窗口句柄
            # print('WindowName:',event.WindowName)    #窗口标题
            # print('Position:',event.Position)        #事件发生时相对于整个屏幕的坐标
            # print('Wheel:',event.Wheel)              #鼠标滚轮
            # print('Injected:',event.Injected)        #判断这个事件是否由程序方式生成，而不是正常的人为触发。
            # print('---')

            if not self.recording or self.running or self.pauserecord:
                return True

            message = event.MessageName
            if message == 'mouse wheel':
                message += ' up' if event.Wheel == 1 else ' down'
            elif message in swapmousemap and swapmousebuttons:
                message = swapmousemap[message]
            all_messages = ('mouse left down', 'mouse left up', 'mouse right down', 'mouse right up', 'mouse move',
                            'mouse middle down', 'mouse middle up', 'mouse wheel up', 'mouse wheel down',
                            # 'mouse x1 down', 'mouse x1 up', 'mouse x2 down', 'mouse x2 up'
                            )
            if message not in all_messages:
                return True

            pos = win32api.GetCursorPos()

            delay = current_ts() - self.ttt

            # 录制鼠标轨迹的精度，数值越小越精准，但同时可能产生大量的冗余
            mouse_move_interval_ms = self.mouse_move_interval_ms.value() or 999999

            if message == 'mouse move' and delay < mouse_move_interval_ms:
                return True

            self.ttt = current_ts()
            if not self.record:
                delay = 0

            x, y = pos
            tx = x / SW
            ty = y / SH
            tpos = (tx, ty)

            print(delay, message, tpos)

            # self.record.append([delay, 'EM', message, tpos])
            self.record.append([delay, 'EM', message, ['{0}%'.format(tx), '{0}%'.format(ty)]])
            self.actioncount = self.actioncount + 1
            text = '%d actions recorded' % self.actioncount

            self.tnumrd.setText(text)
            return True

        def on_keyboard_event(event):

            # print('MessageName:',event.MessageName)          #同上，共同属性不再赘述
            # print('Message:',event.Message)
            # print('Time:',event.Time)
            # print('Window:',event.Window)
            # print('WindowName:',event.WindowName)
            # print('Ascii:', event.Ascii, chr(event.Ascii))   #按键的ASCII码
            # print('Key:', event.Key)                         #按键的名称
            # print('KeyID:', event.KeyID)                     #按键的虚拟键值
            # print('ScanCode:', event.ScanCode)               #按键扫描码
            # print('Extended:', event.Extended)               #判断是否为增强键盘的扩展键
            # print('Injected:', event.Injected)
            # print('Alt', event.Alt)                          #是某同时按下Alt
            # print('Transition', event.Transition)            #判断转换状态
            # print('---')

            message = event.MessageName
            message = message.replace(' sys ', ' ')

            if message == 'key up':
                # listen for start/stop script
                key_name = event.Key.lower()
                # start_name = 'f6'  # as default
                # stop_name = 'f9'  # as default

                hotkeymethod(key_name)

            if not self.recording or self.running or self.pauserecord:
                return True

            all_messages = ('key down', 'key up')
            if message not in all_messages:
                return True

            # 不录制热键
            if event.Key in HOT_KEYS:
                return True

            key_info = (event.KeyID, event.Key, event.Extended)

            delay = current_ts() - self.ttt
            self.ttt = current_ts()
            if not self.record:
                delay = 0

            print(delay, message, key_info)

            self.record.append([delay, 'EK', message, key_info])
            self.actioncount = self.actioncount + 1
            text = '%d actions recorded' % self.actioncount
            self.tnumrd.setText(text)
            return True

        def hotkeymethod(key_name):
            start_index = self.choice_start.currentIndex()
            stop_index = self.choice_stop.currentIndex()
            record_index = self.choice_record.currentIndex()
            # Predict potential conflict
            if start_index == stop_index:
                stop_index = (stop_index + 1) % len(HOT_KEYS)
                self.choice_stop.setCurrentIndex(stop_index)
            if start_index == record_index:
                record_index = (record_index + 1) % len(HOT_KEYS)
                if record_index == stop_index:
                    record_index = (record_index + 1) % len(HOT_KEYS)
                self.choice_record.setCurrentIndex(record_index)
            start_name = HOT_KEYS[start_index].lower()
            stop_name = HOT_KEYS[stop_index].lower()
            record_name = HOT_KEYS[record_index].lower()

            if key_name == start_name and not self.running and not self.recording:
                print('script start')
                # t = RunScriptClass(self, self.pause_event)
                # t.start()
                self.runthread = RunScriptClass(self, self.pause_event)
                self.runthread.start()
                self.isbrokenorfinish = False
                print(key_name, 'host start')
            elif key_name == start_name and self.running and not self.recording:
                if self.paused:
                    print('script resume')
                    self.paused = False
                    self.pause_event.set()
                    print(key_name, 'host resume')
                else:
                    print('script pause')
                    self.paused = True
                    self.pause_event.clear()
                    print(key_name, 'host pause')
            elif key_name == stop_name and self.running and not self.recording:
                print('script stop')
                self.tnumrd.setText('broken')
                self.isbrokenorfinish = True
                if self.paused:
                    self.paused = False
                    self.pause_event.set()
                print(key_name, 'host stop')
            elif key_name == stop_name and self.recording:
                self.recordMethod()
                print(key_name, 'host stop record')
            elif key_name == record_name and not self.running:
                if not self.recording:
                    self.recordMethod()
                    print(key_name, 'host start record')
                else:
                    self.pauseRecordMethod()
                    print(key_name, 'host pause record')
            return key_name in [start_name, stop_name, record_name]

        self.msgdic = {0x0201: 'mouse left down', 0x0202: 'mouse left up',
                       0x0204: 'mouse right down', 0x0205: 'mouse right up',
                       0x0200: 'mouse move',
                       0x0207: 'mouse middle down', 0x0208: 'mouse middle up',
                       0x020a: 'mouse wheel',
                       0x020b: 'mouse x down', 0x020c: 'mouse x up'}
        self.datadic = {0x10000: 'x1', 0x20000: 'x2'}
        self.MyMouseEvent = collections.namedtuple("MyMouseEvent", ["MessageName"])
        self.midashotkey = False

        def mouse_handler(msg, x, y, data, flags, time, hwnd, window_name):
            name = self.msgdic[msg]
            if name == 'mouse wheel':
                name = name + (' up' if data > 0 else ' down')
            elif name in ['mouse x down', 'mouse x up']:
                name = name.replace('x', self.datadic[data])
            if 'mouse x1 down' == name:
                hotkeymethod('xbutton1')
            elif 'mouse x2 down' == name:
                hotkeymethod('xbutton2')
            elif 'mouse middle' in name:
                if 'down' in name:
                    self.midashotkey = hotkeymethod('middle')
                if not self.midashotkey:
                    on_mouse_event(self.MyMouseEvent(name))
            else:
                on_mouse_event(self.MyMouseEvent(name))
            return True

        cpyHook.cSetHook(HookConstants.WH_MOUSE_LL, mouse_handler)
        # self.hm.MouseAll = on_mouse_event
        self.hm.KeyAll = on_keyboard_event
        # self.hm.HookMouse()
        self.hm.HookKeyboard()

    def eventFilter(self, watched, event):
        if event.type() == event.KeyPress or event.type() == event.KeyRelease:
            return True
        return super(UIFunc, self).eventFilter(watched, event)

    def onconfigchange(self):
        self.config.setValue("Config/StartHotKeyIndex", self.choice_start.currentIndex())
        self.config.setValue("Config/StopHotKeyIndex", self.choice_stop.currentIndex())
        self.config.setValue("Config/RecordHotKeyIndex", self.choice_record.currentIndex())
        self.config.setValue("Config/LoopTimes", self.stimes.value())
        self.config.setValue("Config/Precision", self.mouse_move_interval_ms.value())
        self.config.setValue("Config/ExecuteSpeed", self.execute_speed.value())

    def onchangelang(self):
        if self.choice_language.currentText() == '简体中文':
            self.trans.load(get_assets_path('i18n', 'zh-cn'))
            _app = QApplication.instance()
            _app.installTranslator(self.trans)
            self.retranslateUi(self)
        elif self.choice_language.currentText() == 'English':
            self.trans.load(get_assets_path('i18n', 'en'))
            _app = QApplication.instance()
            _app.installTranslator(self.trans)
            self.retranslateUi(self)
        self.retranslateUi(self)
        self.config.setValue("Config/Language", self.choice_language.currentText())

    def closeEvent(self, event):
        self.config.sync()
        event.accept()

    def loadconfig(self):
        if not os.path.exists('config.ini'):
            with open('config.ini', 'w') as f:
                f.write('[Config]\n'
                        'StartHotKeyIndex=3\n'
                        'StopHotKeyIndex=6\n'
                        'RecordHotKeyIndex=7\n'
                        'LoopTimes=1\n'
                        'Precision=200\n'
                        'ExecuteSpeed=100\n'
                        'Language=zh-cn\n')
        return QtCore.QSettings('config.ini', QtCore.QSettings.IniFormat)

    def get_script_path(self):
        i = self.choice_script.currentIndex()
        if i < 0:
            return ''
        script = self.scripts[i]
        path = os.path.join(os.getcwd(), 'scripts', script)
        print(path)
        return path

    def new_script_path(self):
        now = datetime.datetime.now()
        script = '%s.txt' % now.strftime('%m%d_%H%M')
        if script in self.scripts:
            script = '%s.txt' % now.strftime('%m%d_%H%M%S')
        self.scripts.insert(0, script)
        self.choice_script.addItems(self.scripts)
        self.choice_script.setCurrentIndex(0)
        return self.get_script_path()

    def pauseRecordMethod(self):
        if self.pauserecord:
            print('record resume')
            self.pauserecord = False
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Pause', None))
        else:
            print('record pause')
            self.pauserecord = True
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Continue', None))
            self.tnumrd.setText('record paused')

    def OnPauseRecordButton(self):
        self.pauseRecordMethod()

    def recordMethod(self):
        if self.recording:
            print('record stop')
            self.recording = False
            self.record = self.record[:-2]
            output = json.dumps(self.record, indent=1)
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            output = output.replace('\n   ', '').replace('\n  ', '')
            output = output.replace('\n ]', ']')
            open(self.new_script_path(), 'w').write(output)
            self.btrecord.setText(QCoreApplication.translate("UIView", 'Record', None))
            self.tnumrd.setText('finished')
            self.record = []
            self.btpauserecord.setEnabled(False)
            self.btrun.setEnabled(True)
            self.actioncount = 0
            self.pauserecord = False
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Pause Record', None))
        else:
            print('record start')
            self.recording = True
            self.ttt = current_ts()
            status = self.tnumrd.text()
            if 'running' in status or 'recorded' in status:
                return
            self.btrecord.setText(QCoreApplication.translate("UIView", 'Finish', None))
            self.tnumrd.setText('0 actions recorded')
            self.choice_script.setCurrentIndex(-1)
            self.record = []
            self.btpauserecord.setEnabled(True)
            self.btrun.setEnabled(False)

    def OnBtrecordButton(self):
        self.recordMethod()

    def OnBtrunButton(self):
        print('script start by btn')
        # t = RunScriptClass(self, self.pause_event)
        # t.start()
        self.runthread = RunScriptClass(self, self.pause_event)
        self.runthread.start()
        self.isbrokenorfinish = False


class RunScriptClass(threading.Thread):

    def __init__(self, frame: UIFunc, event: threading.Event):
        self.frame = frame
        self.event = event
        self.event.set()
        super(RunScriptClass, self).__init__()

    def run(self):

        status = self.frame.tnumrd.text()
        if self.frame.running or self.frame.recording:
            return

        if 'running' in status or 'recorded' in status:
            return

        script_path = self.frame.get_script_path()
        if not script_path:
            self.frame.tnumrd.setText('script not found, please self.record first!')
            return

        self.frame.running = True

        self.frame.btrun.setEnabled(False)
        self.frame.btrecord.setEnabled(False)

        try:
            self.run_times = self.frame.stimes.value()
            self.running_text = '%s running..' % script_path.split('/')[-1].split('\\')[-1]
            self.frame.tnumrd.setText(self.running_text)
            self.run_speed = self.frame.execute_speed.value()

            self.j = 0
            nointerrupt = True
            while (self.j < self.run_times or self.run_times == 0) and nointerrupt:
                self.j += 1
                current_status = self.frame.tnumrd.text()
                if current_status in ['broken', 'finished']:
                    self.frame.running = False
                    break
                nointerrupt = nointerrupt and RunScriptClass.run_script_once(script_path, self.j, thd=self)
            if nointerrupt:
                self.frame.tnumrd.setText('finished')
            else:
                print('interrupted')
            self.frame.running = False
            PlayPromptTone.play_end_sound()
            print('script run finish!')

        except Exception as e:
            print('run error', e)
            traceback.print_exc()
            self.frame.tnumrd.setText('failed')
            self.frame.running = False
        finally:
            self.frame.btrun.setEnabled(True)
            self.frame.btrecord.setEnabled(True)

    @classmethod
    def run_script_once(cls, script_path, step, thd=None, speed=100):

        content = ''

        lines = []

        try:
            lines = open(script_path, 'r', encoding='utf8').readlines()
        except Exception as e:
            print(e)
            try:
                lines = open(script_path, 'r', encoding='gbk').readlines()
            except Exception as e:
                print(e)

        for line in lines:
            # 去注释
            if '//' in line:
                index = line.find('//')
                line = line[:index]
            # 去空字符
            line = line.strip()
            content += line

        # 去最后一个元素的逗号（如有）
        content = content.replace('],\n]', ']\n]').replace('],]', ']]')

        print(content)
        s = json.loads(content)
        steps = len(s)

        for i in range(steps):
            if thd:
                # current_status = thd.frame.tnumrd.GetLabel()
                # if current_status in ['broken', 'finished']:
                #     break
                if thd.frame.isbrokenorfinish:
                    thd.frame.tnumrd.setText('broken at %d/%d' % (i, steps))
                    return False
                thd.event.wait()
                text = '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i + 1, steps, thd.j, thd.run_times, thd.run_speed)
                thd.frame.tnumrd.setText(text)

            print(s[i])

            delay = s[i][0] / ((thd.run_speed if thd else speed) / 100)
            event_type = s[i][1].upper()
            message = s[i][2].lower()
            action = s[i][3]

            if 1 == step and 0 == i:
                play = PlayPromptTone(1, delay)
                play.start()

            time.sleep(delay / 1000.0)

            if thd:
                # current_status = thd.frame.tnumrd.GetLabel()
                # if current_status in ['broken', 'finished']:
                #     break
                if thd.frame.isbrokenorfinish:
                    thd.frame.tnumrd.setText('broken at %d/%d' % (i + 1, steps))
                    return False
                thd.event.wait()
                text = '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i + 1, steps, thd.j, thd.run_times, thd.run_speed)
                thd.frame.tnumrd.setText(text)

            if event_type == 'EM':
                x, y = action
                # 兼容旧版的绝对坐标
                if not isinstance(x, int) and not isinstance(y, int):
                    x = float(re.match('([0-1].[0-9]+)%', x).group(1))
                    y = float(re.match('([0-1].[0-9]+)%', y).group(1))

                if action == [-1, -1]:
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

                if message == 'mouse left down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                elif message == 'mouse left up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif message == 'mouse right down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                elif message == 'mouse right up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                elif message == 'mouse middle down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, 0, 0, 0, 0)
                elif message == 'mouse middle up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, 0, 0, 0, 0)
                elif message == 'mouse wheel up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, win32con.WHEEL_DELTA, 0)
                elif message == 'mouse wheel down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -win32con.WHEEL_DELTA, 0)
                elif message == 'mouse move':
                    pass
                else:
                    print('unknow mouse event:', message)

            elif event_type == 'EK':
                key_code, key_name, extended = action

                # shift ctrl alt
                # if key_code >= 160 and key_code <= 165:
                #     key_code = int(key_code/2) - 64

                # 不执行热键
                if key_name in HOT_KEYS:
                    continue

                base = 0
                if extended:
                    base = win32con.KEYEVENTF_EXTENDEDKEY

                if message == 'key down':
                    win32api.keybd_event(key_code, 0, base, 0)
                elif message == 'key up':
                    win32api.keybd_event(key_code, 0, base | win32con.KEYEVENTF_KEYUP, 0)
                else:
                    print('unknow keyboard event:', message)

            elif event_type == 'EX':

                if message == 'input':
                    text = action
                    pyperclip.copy(text)
                    # Ctrl+V
                    win32api.keybd_event(162, 0, 0, 0)  # ctrl
                    win32api.keybd_event(86, 0, 0, 0)  # v
                    win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event(162, 0, win32con.KEYEVENTF_KEYUP, 0)
                else:
                    print('unknow extra event:', message)
        return True

class PlayPromptTone(threading.Thread):

    def __init__(self, op, delay):
        self._delay = delay
        self._op = op
        super().__init__()

    def run(self):
        if 1 == self._op:
            if self._delay >= 1000:
                time.sleep((self._delay - 500.0) / 1000.0)
            self._play_start_sound()

    def _play_start_sound(self):
        try:
            path = get_assets_path('sounds', 'start.mp3')
            playsound(path)
        except PlaysoundException as e:
            print(e)

    @classmethod
    def play_end_sound(cls):
        try:
            path = get_assets_path('sounds', 'end.mp3')
            playsound(path)
        except PlaysoundException as e:
            print(e)
