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
from importlib.machinery import SourceFileLoader

import pyWinhook
import pyperclip
import win32api
import win32con
from PySide2.QtCore import QSettings, Qt
from PySide2.QtCore import QTranslator, QCoreApplication
from PySide2.QtWidgets import QMainWindow, QApplication
from loguru import logger
from playsound import playsound, PlaysoundException
from pyWinhook import cpyHook, HookConstants
from win32gui import GetDC
from win32print import GetDeviceCaps

from UIView import Ui_UIView
from assets.plugins.ProcessException import *

os.environ['QT_ENABLE_HIGHDPI_SCALING'] = "1"
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
            'XButton1', 'XButton2', 'Middle']
hDC = GetDC(0)
SW = GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
SH = GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)

# 是否切换主要/次要功能键
swapmousebuttons = True if winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                                              r'Control Panel\Mouse',
                                                              0,
                                                              winreg.KEY_READ),
                                               'SwapMouseButtons')[0] == '1' else False
swapmousemap = {'mouse left down': 'mouse right down', 'mouse left up': 'mouse right up',
                'mouse right down': 'mouse left down', 'mouse right up': 'mouse left up'}

logger.remove()
logger.add(sys.stdout, backtrace=True, diagnose=True,
           level='DEBUG')
logger.add('logs/{time}.log', rotation='20MB', backtrace=True, diagnose=True,
           level='INFO')


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

        logger.info('assets root:{0}'.format(get_assets_path()))

        self.setupUi(self)

        self.config = self.loadconfig()

        self.setFocusPolicy(Qt.NoFocus)

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

        self.choice_extension.addItems(['Extension'])
        if not os.path.exists('plugins'):
            os.mkdir('plugins')
        for i in os.listdir('plugins'):
            if i[-3:] == '.py':
                self.choice_extension.addItems([i[:-3]])

        self.choice_start.addItems(HOT_KEYS)
        self.choice_stop.addItems(HOT_KEYS)
        self.choice_record.addItems(HOT_KEYS)
        self.choice_start.setCurrentIndex(int(self.config.value("Config/StartHotKeyIndex")))
        self.choice_stop.setCurrentIndex(int(self.config.value("Config/StopHotKeyIndex")))
        self.choice_record.setCurrentIndex(int(self.config.value("Config/RecordHotKeyIndex")))
        self.stimes.setValue(int(self.config.value("Config/LoopTimes")))
        self.mouse_move_interval_ms.setValue(int(self.config.value("Config/Precision")))
        self.execute_speed.setValue(int(self.config.value("Config/ExecuteSpeed")))
        self.choice_extension.setCurrentText(self.config.value("Config/Extension"))
        self.choice_start.currentIndexChanged.connect(self.onconfigchange)
        self.choice_stop.currentIndexChanged.connect(self.onconfigchange)
        self.choice_record.currentIndexChanged.connect(self.onconfigchange)
        self.stimes.valueChanged.connect(self.onconfigchange)
        self.execute_speed.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(self.onconfigchange)
        self.choice_extension.currentIndexChanged.connect(self.onconfigchange)

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
        self.choice_extension.installEventFilter(self)

        self.extension = None

        self.hm = pyWinhook.HookManager()

        # 鼠标操作录制逻辑
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

            sevent = ScriptEvent({
                'delay': delay,
                'event_type': 'EM',
                'message': message,
                'action': tpos,
                'addon': None
            })
            if self.extension.onrecord(sevent, self.actioncount):
                # self.record.append([delay, 'EM', message, tpos])
                tx, ty = sevent.action
                if sevent.addon:
                    self.record.append(
                        [sevent.delay, sevent.event_type, sevent.message, ['{0}%'.format(tx), '{0}%'.format(ty)],
                         sevent.addon])
                else:
                    self.record.append(
                        [sevent.delay, sevent.event_type, sevent.message, ['{0}%'.format(tx), '{0}%'.format(ty)]])
                self.actioncount = self.actioncount + 1
                text = '%d actions recorded' % self.actioncount
                logger.debug('Recorded %s' % sevent)
                self.tnumrd.setText(text)

            return True

        # 键盘操作录制逻辑
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

            sevent = ScriptEvent({
                'delay': delay,
                'event_type': 'EK',
                'message': message,
                'action': key_info,
                'addon': None
            })
            if self.extension.onrecord(sevent, self.actioncount):
                logger.debug('Recorded %s' % sevent)
                # self.record.append([delay, 'EK', message, key_info])
                if sevent.addon:
                    self.record.append(
                        [sevent.delay, sevent.event_type, sevent.message, sevent.action,
                         sevent.addon])
                else:
                    self.record.append(
                        [sevent.delay, sevent.event_type, sevent.message, sevent.action])
                self.actioncount = self.actioncount + 1
                text = '%d actions recorded' % self.actioncount
                self.tnumrd.setText(text)

            return True

        # 热键响应逻辑
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
                logger.info('Script start')
                self.runthread = RunScriptClass(self, self.pause_event)
                self.runthread.start()
                self.isbrokenorfinish = False
                logger.debug('{0} host start'.format(key_name))
            elif key_name == start_name and self.running and not self.recording:
                if self.paused:
                    logger.info('Script resume')
                    self.paused = False
                    self.pause_event.set()
                    logger.debug('{0} host resume'.format(key_name))
                else:
                    logger.info('Script pause')
                    self.paused = True
                    self.pause_event.clear()
                    logger.debug('{0} host pause'.format(key_name))
            elif key_name == stop_name and self.running and not self.recording:
                logger.info('Script stop')
                self.tnumrd.setText('broken')
                self.isbrokenorfinish = True
                if self.paused:
                    self.paused = False
                    self.pause_event.set()
                logger.debug('{0} host stop'.format(key_name))
            elif key_name == stop_name and self.recording:
                self.recordMethod()
                logger.info('Record stop')
                logger.debug('{0} host stop record'.format(key_name))
            elif key_name == record_name and not self.running:
                if not self.recording:
                    self.recordMethod()
                    logger.info('Record start')
                    logger.debug('{0} host start record'.format(key_name))
                else:
                    self.pauseRecordMethod()
                    logger.info('Record pause')
                    logger.debug('{0} host pause record'.format(key_name))
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

        # 使用一般的HookMouse无法捕获鼠标侧键操作，因此采用cpyHook捕获鼠标操作
        def mouse_handler(msg, x, y, data, flags, time, hwnd, window_name):
            if self.recording:
                try:
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
                except KeyError as e:
                    logger.debug('Unknown mouse event, keyid {0}'.format(e))
                finally:
                    return True
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
        self.config.setValue("Config/Extension", self.choice_extension.currentText())

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
            with open('config.ini', 'w', encoding='utf-8') as f:
                f.write('[Config]\n'
                        'StartHotKeyIndex=3\n'
                        'StopHotKeyIndex=6\n'
                        'RecordHotKeyIndex=7\n'
                        'LoopTimes=1\n'
                        'Precision=200\n'
                        'ExecuteSpeed=100\n'
                        'Language=zh-cn\n'
                        'Extension=Extension\n')
        return QSettings('config.ini', QSettings.IniFormat)

    def get_script_path(self):
        i = self.choice_script.currentIndex()
        if i < 0:
            return ''
        script = self.scripts[i]
        path = os.path.join(os.getcwd(), 'scripts', script)
        logger.info('Script path: {0}'.format(path))
        return path

    def new_script_path(self):
        now = datetime.datetime.now()
        script = '%s.txt' % now.strftime('%m%d_%H%M')
        if script in self.scripts:
            script = '%s.txt' % now.strftime('%m%d_%H%M%S')
        self.scripts.insert(0, script)
        self.choice_script.clear()
        self.choice_script.addItems(self.scripts)
        self.choice_script.setCurrentIndex(0)
        return self.get_script_path()

    def pauseRecordMethod(self):
        if self.pauserecord:
            logger.info('Record resume')
            self.pauserecord = False
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Pause', None))
        else:
            logger.info('Record resume')
            self.pauserecord = True
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Continue', None))
            self.tnumrd.setText('record paused')

    def OnPauseRecordButton(self):
        self.pauseRecordMethod()

    def recordMethod(self):
        if self.recording:
            logger.info('Record stop')
            self.recording = False
            output = json.dumps(self.record, indent=1, ensure_ascii=False)
            output = output.replace('\r\n', '\n').replace('\r', '\n')
            output = output.replace('\n   ', '').replace('\n  ', '')
            output = output.replace('\n ]', ']')
            with open(self.new_script_path(), 'w', encoding='utf-8') as f:
                f.write(output)
            self.btrecord.setText(QCoreApplication.translate("UIView", 'Record', None))
            self.tnumrd.setText('finished')
            self.record = []
            self.btpauserecord.setEnabled(False)
            self.btrun.setEnabled(True)
            self.actioncount = 0
            self.pauserecord = False
            self.choice_script.setCurrentIndex(0)
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Pause Record', None))
        else:
            self.extension = RunScriptClass.getextension(self.choice_extension.currentText(),
                                                         runtimes=self.stimes.value(),
                                                         speed=self.execute_speed.value())
            logger.info('Record start')
            self.recording = True
            self.ttt = current_ts()
            status = self.tnumrd.text()
            if 'running' in status or 'recorded' in status:
                return
            self.btrecord.setText(QCoreApplication.translate("UIView", 'Finish', None))
            self.tnumrd.setText('0 actions recorded')
            self.record = []
            self.btpauserecord.setEnabled(True)
            self.btrun.setEnabled(False)

    def OnBtrecordButton(self):
        if self.recording:
            self.record = self.record[:-2]
        self.recordMethod()

    def OnBtrunButton(self):
        logger.info('Script start')
        logger.debug('Script start by btn')
        self.runthread = RunScriptClass(self, self.pause_event)
        self.runthread.start()
        self.isbrokenorfinish = False


class RunScriptClass(threading.Thread):

    def __init__(self, frame: UIFunc, event: threading.Event):
        self.frame = frame
        self.event = event
        self.event.set()
        super(RunScriptClass, self).__init__()

    @logger.catch
    def run(self):

        status = self.frame.tnumrd.text()
        if self.frame.running or self.frame.recording:
            return

        if 'running' in status or 'recorded' in status:
            return

        script_path = self.frame.get_script_path()
        if not script_path:
            self.frame.tnumrd.setText('script not found, please self.record first!')
            logger.warning('Script not found, please record first!')
            return

        self.frame.running = True

        self.frame.btrun.setEnabled(False)
        self.frame.btrecord.setEnabled(False)
        try:
            self.running_text = '%s running..' % script_path.split('/')[-1].split('\\')[-1]
            self.frame.tnumrd.setText(self.running_text)
            logger.info('%s running..' % script_path.split('/')[-1].split('\\')[-1])

            # 解析脚本，返回事件集合与扩展类对象
            logger.debug('Parse script..')
            events, module_name = RunScriptClass.parsescript(script_path, speed=self.frame.execute_speed.value())
            extension = RunScriptClass.getextension(
                module_name if module_name is not None else self.frame.choice_extension.currentText(),
                runtimes=self.frame.stimes.value(),
                speed=self.frame.execute_speed.value(),
                thd=self
                )

            self.j = 0
            nointerrupt = True
            logger.debug('Run script..')
            PlayPromptTone(1, 0).start()
            while (self.j < extension.runtimes or extension.runtimes == 0) and nointerrupt:
                logger.info('===========%d==============' % self.j)
                current_status = self.frame.tnumrd.text()
                if current_status in ['broken', 'finished']:
                    self.frame.running = False
                    break
                try:
                    if extension.onbeforeeachloop(self.j):
                        nointerrupt = nointerrupt and RunScriptClass.run_script_once(events, extension, thd=self)
                    else:
                        nointerrupt = True
                    extension.onaftereachloop(self.j)
                    self.j += 1
                except BreakProcess:
                    logger.debug('Break')
                    self.j += 1
                    continue
                except EndProcess:
                    logger.debug('End')
                    break
            extension.onendp()
            if nointerrupt:
                self.frame.tnumrd.setText('finished')
                logger.info('Script run finish')
            else:
                logger.info('Script run interrupted')
            self.frame.running = False
            PlayPromptTone.play_end_sound()

        except Exception as e:
            logger.error('Run error {0}'.format(e))
            traceback.print_exc()
            self.frame.tnumrd.setText('failed')
            self.frame.running = False
        finally:
            self.frame.btrun.setEnabled(True)
            self.frame.btrecord.setEnabled(True)

    # 获取扩展实例
    @classmethod
    @logger.catch
    def getextension(cls, module_name='Extension', runtimes=1, speed=100, thd=None, swap=None):
        if module_name == 'Extension':
            module = SourceFileLoader(module_name, get_assets_path('plugins', 'Extension.py')).load_module()
        else:
            module = SourceFileLoader(module_name,
                                      os.path.join(os.getcwd(), 'plugins', '%s.py' % module_name)).load_module()
        module_cls = getattr(module, module_name)
        logger.info('Loaded plugin class {0} in module {1}'.format(module_cls, module_name))
        return module_cls(runtimes, speed, thd, swap)

    # 解析脚本内容，转换为ScriptEvent集合
    @classmethod
    def parsescript(cls, script_path, speed=100):
        content = ''
        lines = []
        try:
            with open(script_path, 'r', encoding='utf8') as f:
                lines = f.readlines()
        except Exception as e:
            logger.warning(e)
            try:
                with open(script_path, 'r', encoding='gbk') as f:
                    lines = f.readlines()
            except Exception as e:
                logger.error(e)

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

        logger.debug('Script content')
        logger.debug(content)
        s = json.loads(content)
        steps = len(s)

        events = []
        startindex = 0
        module_name = None
        if steps >= 1 and re.match('\[.+\]', str(s[0])) is None:
            module_name = s[0]
            startindex = 1
        for i in range(startindex, steps):
            delay = s[i][0] / (speed / 100)
            event_type = s[i][1].upper()
            message = s[i][2].lower()
            action = s[i][3]
            addon = None
            if len(s[i]) > 4:
                addon = s[i][4]
            events.append(ScriptEvent({
                'delay': delay,
                'event_type': event_type,
                'message': message,
                'action': action,
                'addon': addon
            }))
        return events, module_name

    @classmethod
    def run_sub_script(cls, extension, scriptpath: str, subextension_name: str = 'Extension',
                        runtimes: int = 1, speed: int = 100, thd=None):
        newevents, module_name = RunScriptClass.parsescript(scriptpath, speed=speed)
        newextension = RunScriptClass.getextension(
            module_name if module_name is not None else subextension_name,
            runtimes=runtimes,
            speed=speed,
            swap=extension.swap,
            thd=thd
            )
        logger.info('Script path:%s' % scriptpath)
        k = 0
        nointerrupt = True
        while (k < newextension.runtimes or newextension.runtimes == 0) and nointerrupt:
            logger.info('========%d========' % k)
            try:
                if newextension.onbeforeeachloop(k):
                    nointerrupt = nointerrupt and RunScriptClass.run_script_once(newevents, newextension, thd)
                newextension.onaftereachloop(k)
                k += 1
            except BreakProcess:
                logger.debug('Break')
                k += 1
                continue
            except EndProcess:
                logger.debug('End')
                break
        newextension.onendp()
        extension.swap = newextension.swap
        if nointerrupt:
            logger.info('Subscript run finish')
        else:
            logger.info('Subscript run interrupted at loop %d' % k)

    # 执行集合中的ScriptEvent
    @classmethod
    def run_script_once(cls, events, extension, thd=None):
        steps = len(events)
        i = 0
        while i < steps:
            if thd:
                if thd.frame.isbrokenorfinish:
                    logger.info('Broken at %d/%d' % (i, steps))
                    thd.frame.tnumrd.setText('broken at %d/%d' % (i, steps))
                    return False
                thd.event.wait()
                text = '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i + 1, steps, thd.j + 1, extension.runtimes, extension.speed)
                logger.trace(
                    '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i + 1, steps, thd.j + 1, extension.runtimes, extension.speed))
                thd.frame.tnumrd.setText(text)

            event = events[i]

            try:
                flag = extension.onrunbefore(event, i)
                if flag:
                    logger.debug(event)
                    event.execute()
                else:
                    logger.debug('Skipped %d' % i)
                extension.onrunafter(event, i)
                i = i + 1
            except JumpProcess as jp:
                if jp.index < 0:
                    logger.error('Jump index out of range: %d' % jp.index)
                elif jp.index >= steps:
                    logger.warning('Jump index exceed events range: %d/%d, ends current loop' % (jp.index, steps))
                    break
                else:
                    i = jp.index
                    logger.debug('Jump at %d' % i)
                    continue

            if thd:
                if thd.frame.isbrokenorfinish:
                    thd.frame.tnumrd.setText('broken at %d/%d' % (i, steps))
                    logger.info('Broken at %d/%d' % (i, steps))
                    return False
                thd.event.wait()
                text = '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i + 1, steps, thd.j + 1, extension.runtimes, extension.speed)
                logger.trace(
                    '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i + 1, steps, thd.j + 1, extension.runtimes, extension.speed))
                thd.frame.tnumrd.setText(text)

        return True


class ScriptEvent:
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

    # 执行操作
    def execute(self):
        time.sleep(self.delay / 1000.0)

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
            if key_name in HOT_KEYS:
                return

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
            logger.error(e)

    @classmethod
    def play_end_sound(cls):
        try:
            path = get_assets_path('sounds', 'end.mp3')
            playsound(path)
        except PlaysoundException as e:
            logger.error(e)
