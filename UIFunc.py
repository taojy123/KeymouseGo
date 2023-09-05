# -*- encoding:utf-8 -*-
import datetime
import json
import os
import re
import sys
import threading
import traceback
import platform
import locale
import Recorder
from importlib.machinery import SourceFileLoader

from PySide6.QtGui import QTextCursor
from qt_material import list_themes, QtStyleTools
from PySide6.QtCore import *
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtMultimedia import QSoundEffect
from loguru import logger

from Event import ScriptEvent, flag_multiplemonitor
from UIView import Ui_UIView
from assets.plugins.ProcessException import *

from KeymouseGo import to_abs_path

mutex = QMutex()
cond = QWaitCondition()

os.environ['QT_ENABLE_HIGHDPI_SCALING'] = "1"
if platform.system() == 'Windows':
    HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                'XButton1', 'XButton2', 'Middle']
else:
    HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                'Middle']

logger.remove()
if sys.stdout is not None:
    logger.add(sys.stdout, backtrace=True, diagnose=True,
               level='DEBUG')
logger.add(to_abs_path('logs', '{time}.log'), rotation='20MB', backtrace=True, diagnose=True,
           level='INFO')


def get_assets_path(*paths):
    # pyinstaller -F --add-data ./assets;assets KeymouseGo.py
    try:
        root = sys._MEIPASS
    except:
        root = os.getcwd()
    return os.path.join(root, 'assets', *paths)


scripts = []
scripts_map = {'current_index': 0, 'choice_language': '简体中文'}


def get_script_list_from_dir():
    global scripts

    if not os.path.exists(to_abs_path('scripts')):
        os.mkdir(to_abs_path('scripts'))
    scripts = os.listdir(to_abs_path('scripts'))[::-1]
    scripts = list(filter(lambda s: s.endswith('.txt'), scripts))


def update_script_map():
    global scripts_map
    
    for (i, item) in enumerate(scripts):
        scripts_map[item] = i


class UIFunc(QMainWindow, Ui_UIView, QtStyleTools):
    def __init__(self, app):
        global scripts

        super(UIFunc, self).__init__()

        logger.info('assets root:{0}'.format(get_assets_path()))

        self.setupUi(self)

        self.app = app

        self.config = self.loadconfig()

        self.setFocusPolicy(Qt.NoFocus)

        self.trans = QTranslator(self)
        self.choice_language.addItems(['简体中文', 'English'])
        self.choice_language.currentTextChanged.connect(self.onchangelang)

        # 获取默认的地区设置
        language = '简体中文' if locale.getdefaultlocale()[0] == 'zh_CN' else 'English'
        self.choice_language.setCurrentText(language)
        self.onchangelang()

        get_script_list_from_dir()
        update_script_map()
        self.scripts = scripts
        self.choice_script.addItems(self.scripts)
        if self.scripts:
            self.choice_script.setCurrentIndex(0)

        self.choice_extension.addItems(['Extension'])
        if not os.path.exists(to_abs_path('plugins')):
            os.mkdir(to_abs_path('plugins'))
        for i in os.listdir(to_abs_path('plugins')):
            if i[-3:] == '.py':
                self.choice_extension.addItems([i[:-3]])

        self.choice_theme.addItems(list_themes())
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
        self.choice_theme.setCurrentText(self.config.value("Config/Theme"))
        if self.config.value('Config/Script') is not None and self.config.value('Config/Script') in self.scripts:
            self.choice_script.setCurrentText(self.config.value('Config/Script'))
        self.choice_start.currentIndexChanged.connect(self.onconfigchange)
        self.choice_stop.currentIndexChanged.connect(self.onconfigchange)
        self.choice_record.currentIndexChanged.connect(self.onconfigchange)
        self.stimes.valueChanged.connect(self.onconfigchange)
        self.execute_speed.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(Recorder.set_interval)
        self.choice_extension.currentIndexChanged.connect(self.onconfigchange)
        self.choice_theme.currentTextChanged.connect(self.onchangetheme)
        self.choice_script.currentTextChanged.connect(self.onconfigchange)

        self.onchangetheme()

        self.textlog.textChanged.connect(lambda: self.textlog.moveCursor(QTextCursor.End))

        # For tune playing
        self.player = QSoundEffect()
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(
            lambda: self.player.setVolume(
                self.volumeSlider.value()/100.0))

        self.running = False
        self.recording = False
        self.record = []

        # for pause-resume feature
        self.paused = False

        # Pause-Resume Record
        self.pauserecord = False

        self.actioncount = 0

        # For better thread control
        self.runthread = None
        self.is_broken_or_finish = True

        self.btrun.clicked.connect(self.OnBtrunButton)
        self.btrecord.clicked.connect(self.OnBtrecordButton)
        self.btpauserecord.clicked.connect(self.OnPauseRecordButton)
        self.bt_open_script_files.clicked.connect(self.OnBtOpenScriptFilesButton)
        self.choice_record.installEventFilter(self)
        self.choice_language.installEventFilter(self)
        self.choice_stop.installEventFilter(self)
        self.choice_script.installEventFilter(self)
        self.choice_start.installEventFilter(self)
        self.btrun.installEventFilter(self)
        self.btrecord.installEventFilter(self)
        self.btpauserecord.installEventFilter(self)
        self.bt_open_script_files.installEventFilter(self)
        self.choice_extension.installEventFilter(self)

        self.extension = None

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
                self.textlog.clear()
                self.runthread = RunScriptClass(self)
                self.runthread.start()
                self.is_broken_or_finish = False
                logger.debug('{0} host start'.format(key_name))
            elif key_name == start_name and self.running and not self.recording:
                if self.paused:
                    logger.info('Script resume')
                    self.paused = False
                    self.runthread.resume()
                    logger.debug('{0} host resume'.format(key_name))
                else:
                    logger.info('Script pause')
                    self.paused = True
                    self.runthread.eventPause = True
                    logger.debug('{0} host pause'.format(key_name))
            elif key_name == stop_name and self.running and not self.recording:
                logger.info('Script stop')
                self.tnumrd.setText('broken')
                self.is_broken_or_finish = True
                if self.paused:
                    self.paused = False
                self.runthread.resume()
                logger.debug('{0} host stop'.format(key_name))
            elif key_name == stop_name and self.recording:
                self.recordMethod()
                logger.info('Record stop')
                logger.debug('{0} host stop record'.format(key_name))
            elif key_name == record_name and not self.running:
                if not self.recording:
                    self.recordMethod()
                    # logger.info('Record start')
                    logger.debug('{0} host start record'.format(key_name))
                else:
                    self.pauseRecordMethod()
                    # logger.info('Record pause')
                    logger.debug('{0} host pause record'.format(key_name))
            return key_name in [start_name, stop_name, record_name]

        @Slot(ScriptEvent)
        def on_record_event(event: ScriptEvent):
            # 判断mouse热键
            if event.event_type == "EM":
                name = event.message
                if 'mouse x1 down' == name and hotkeymethod('xbutton1'):
                    return
                elif 'mouse x2 down' == name and hotkeymethod('xbutton2'):
                    return
                elif 'mouse middle down' == name and hotkeymethod('middle'):
                    return
            else:
                key_name = event.action[1]
                if event.message == 'key down':
                    # listen for start/stop script
                    # start_name = 'f6'  # as default
                    # stop_name = 'f9'  # as default
                    hotkeymethod(key_name.lower())
                # 不录制热键
                if key_name in HOT_KEYS:
                    return
            # 录制事件
            if not (not self.recording or self.running or self.pauserecord):
                if self.extension.onrecord(event, self.actioncount):
                    if event.event_type == 'EM' and not flag_multiplemonitor:
                        record = [event.delay, event.event_type, event.message]
                        tx, ty = event.action
                        record.append(['{0}%'.format(tx), '{0}%'.format(ty)])
                    else:
                        record = [event.delay, event.event_type, event.message,
                                  event.action]
                    if event.addon:
                        record.append(event.addon)
                    self.record.append(record)
                    self.actioncount = self.actioncount + 1
                    text = '%d actions recorded' % self.actioncount
                    logger.debug('Recorded %s' % event)
                    self.tnumrd.setText(text)
        logger.debug('Initialize at thread ' + str(threading.currentThread()))
        Recorder.setuphook()
        Recorder.set_callback(on_record_event)
        Recorder.set_interval(self.mouse_move_interval_ms.value())

    def eventFilter(self, watched, event: QEvent):
        et: QEvent.Type = event.type()
        # print(event, et)
        if et == QEvent.KeyPress or et == QEvent.KeyRelease:
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
        self.config.setValue("Config/Theme", self.choice_theme.currentText())
        self.config.setValue("Config/Script", self.choice_script.currentText())

    def onchangelang(self):
        global scripts_map

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

    def onchangetheme(self):
        self.apply_stylesheet(self.app, theme=self.choice_theme.currentText())
        self.config.setValue("Config/Theme", self.choice_theme.currentText())

    def playtune(self, filename: str):
        self.player.setSource(QUrl.fromLocalFile(get_assets_path('sounds', filename)))
        self.player.play()

    def closeEvent(self, event):
        self.config.sync()
        if self.running:
            self.is_broken_or_finish = True
            if self.paused:
                self.paused = False
            self.runthread.resume()
        event.accept()

    def loadconfig(self):
        if not os.path.exists(to_abs_path('config.ini')):
            with open(to_abs_path('config.ini'), 'w', encoding='utf-8') as f:
                f.write('[Config]\n'
                        'StartHotKeyIndex=3\n'
                        'StopHotKeyIndex=6\n'
                        'RecordHotKeyIndex=7\n'
                        'LoopTimes=1\n'
                        'Precision=200\n'
                        'ExecuteSpeed=100\n'
                        'Language=zh-cn\n'
                        'Extension=Extension\n'
                        'Theme=light_cyan_500.xml\n')
        return QSettings(to_abs_path('config.ini'), QSettings.IniFormat)

    def get_script_path(self):
        i = self.choice_script.currentIndex()
        if i < 0:
            return ''
        script = self.scripts[i]
        path = os.path.join(to_abs_path('scripts'), script)
        logger.info('Script path: {0}'.format(path))
        return path

    def new_script_path(self):
        now = datetime.datetime.now()
        script = '%s.txt' % now.strftime('%m%d_%H%M')
        if script in self.scripts:
            script = '%s.txt' % now.strftime('%m%d_%H%M%S')
        self.scripts.insert(0, script)
        update_script_map()
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
            logger.info('Record pause')
            self.pauserecord = True
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Continue', None))
            self.tnumrd.setText('record paused')

    def OnPauseRecordButton(self):
        self.pauseRecordMethod()

    def OnBtOpenScriptFilesButton(self):
        global scripts_map

        import UIFileDialogFunc

        scripts_map['current_index'] = self.choice_script.currentIndex()
        file_dialog = UIFileDialogFunc.FileDialog()
        self.bt_open_script_files.setDisabled(True)
        self.btrecord.setDisabled(True)
        self.btrun.setDisabled(True)
        file_dialog.show()
        self.bt_open_script_files.setDisabled(False)
        self.btrecord.setDisabled(False)
        self.btrun.setDisabled(False)
        # 重新设置的为点击按钮时, 所处的位置
        self.choice_script.clear()
        self.choice_script.addItems(scripts)
        self.choice_script.setCurrentIndex(scripts_map['current_index'])

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
            self.textlog.clear()
            self.recording = True
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
        self.textlog.clear()
        self.runthread = RunScriptClass(self)
        self.runthread.start()
        self.is_broken_or_finish = False


class RunScriptClass(QThread):
    logSignal = Signal(str)
    tnumrdSignal = Signal(str)
    btnSignal = Signal(bool)

    def __init__(self, frame: UIFunc):
        super().__init__()
        logger.debug('Thread created at thread' + str(threading.currentThread()))
        self.frame = frame
        self.eventPause = False

        # 更新控件的槽函数
        self.logSignal.connect(frame.textlog.append)
        self.tnumrdSignal.connect(frame.tnumrd.setText)
        self.btnSignal.connect(frame.btrun.setEnabled)
        self.btnSignal.connect(frame.btrecord.setEnabled)

    def pause(self):
        mutex.lock()
        cond.wait(mutex)
        mutex.unlock()

    def sleep(self, msecs: int):
        mutex.lock()
        cond.wait(mutex, QDeadlineTimer(int(msecs)))
        mutex.unlock()

    def resume(self):
        self.eventPause = False
        mutex.lock()
        cond.wakeAll()
        mutex.unlock()

    def wait_if_pause(self):
        if self.eventPause:
            self.pause()
        else:
            self.resume()

    @logger.catch
    def run(self):
        status = self.frame.tnumrd.text()
        if self.frame.running or self.frame.recording:
            return

        if 'running' in status or 'recorded' in status:
            return

        script_path = self.frame.get_script_path()
        if not script_path:
            self.tnumrdSignal.emit('script not found, please self.record first!')
            logger.warning('Script not found, please record first!')
            return

        self.frame.running = True

        self.btnSignal.emit(False)
        try:
            self.running_text = '%s running..' % script_path.split('/')[-1].split('\\')[-1]
            self.tnumrdSignal.emit(self.running_text)
            logger.info('%s running..' % script_path.split('/')[-1].split('\\')[-1])

            # 解析脚本，返回事件集合与扩展类对象
            logger.debug('Parse script..')
            try:
                events, module_name, labeldict = RunScriptClass.parsescript(script_path,
                                                                            speed=self.frame.execute_speed.value())
            except Exception as e:
                logger.error(e)
                self.logSignal.emit('==============\nAn error occurred while parsing script')
                self.logSignal.emit(str(e))
                self.logSignal.emit('==============')
            extension = RunScriptClass.getextension(
                module_name if module_name is not None else self.frame.choice_extension.currentText(),
                runtimes=self.frame.stimes.value(),
                speed=self.frame.execute_speed.value(),
                thd=self
            )

            self.j = 0
            nointerrupt = True
            logger.debug('Run script..')
            extension.onbeginp()
            self.frame.playtune('start.wav')
            while (self.j < extension.runtimes or extension.runtimes == 0) and nointerrupt:
                logger.debug('===========%d==============' % self.j)
                current_status = self.frame.tnumrd.text()
                if current_status in ['broken', 'finished']:
                    self.frame.running = False
                    break
                self.tnumrdSignal.emit('{0}... Looptimes [{1}/{2}]'.format(
                    self.running_text, self.j + 1, extension.runtimes))
                try:
                    if extension.onbeforeeachloop(self.j):
                        nointerrupt = nointerrupt and RunScriptClass.run_script_once(events, extension, thd=self,
                                                                                     labeldict=labeldict)
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
            self.frame.playtune('end.wav')
            if nointerrupt:
                self.tnumrdSignal.emit('finished')
                logger.info('Script run finish')
            else:
                logger.info('Script run interrupted')
            self.frame.running = False

        except Exception as e:
            logger.error('Run error: {0}'.format(e))
            traceback.print_exc()
            self.logSignal.emit('==============\nAn error occurred during runtime')
            self.logSignal.emit(str(e))
            self.logSignal.emit('==============')
            self.logSignal.emit('failed')
            self.frame.running = False
        finally:
            self.btnSignal.emit(True)

    # 获取扩展实例
    @classmethod
    @logger.catch
    def getextension(cls, module_name='Extension', runtimes=1, speed=100, thd=None, swap=None):
        if module_name == 'Extension':
            module = SourceFileLoader(module_name, get_assets_path('plugins', 'Extension.py')).load_module()
        else:
            module = SourceFileLoader(module_name,
                                      os.path.join(to_abs_path('plugins', '%s.py' % module_name))).load_module()
        module_cls = getattr(module, module_name)
        logger.info('Load plugin class {0} in module {1}'.format(module_cls, module_name))
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
        numoflabels = 0
        labeldict = {'Start': 0}
        # 识别标签或脚本语句
        for i in range(startindex, steps):
            if type(s[i]) == str:
                labeldict[s[i]] = i - numoflabels - startindex
                numoflabels = numoflabels + 1
            else:
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
        return events, module_name, labeldict

    @classmethod
    def run_sub_script(cls, extension, scriptpath: str, subextension_name: str = 'Extension',
                        runtimes: int = 1, speed: int = 100, thd=None, labeldict=None):
        newevents, module_name, label_dict = RunScriptClass.parsescript(scriptpath, speed=speed)
        if labeldict is None:
            labeldict = label_dict
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
            logger.debug('========%d========' % k)
            try:
                if newextension.onbeforeeachloop(k):
                    nointerrupt = nointerrupt and RunScriptClass.run_script_once(newevents, newextension, thd=thd, labeldict=labeldict)
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
    def run_script_once(cls, events, extension, thd=None, labeldict=None):
        steps = len(events)
        i = 0
        while i < steps:
            if thd:
                if thd.frame.is_broken_or_finish:
                    logger.info('Broken at [%d/%d]' % (i, steps))
                    return False
                thd.wait_if_pause()
                logger.trace(
                    '%s  [%d/%d %d/%d] %d%%' % (thd.running_text, i + 1, steps, thd.j + 1, extension.runtimes, extension.speed))
                thd.logSignal.emit('{0} [{1}/{2}]'.format(
                            events[i].summarystr(), i + 1, steps))

            event = events[i]

            try:
                flag = extension.onrunbefore(event, i)
                if flag:
                    logger.debug(event)
                    event.execute(thd)
                else:
                    logger.debug('Skipped %d' % i)
                extension.onrunafter(event, i)
                i = i + 1
            except JumpProcess as jp:
                if labeldict is not None:
                    index = labeldict.get(jp.index, None)
                    if index is not None:
                        logger.debug('Jump at label %s, i.e. line %i' % (jp.index, index))
                        jp.index = index
                    else:
                        logger.error('Invalid Jump Label')
                        raise Exception('Invalid Jump Label')
                if jp.index < 0:
                    logger.error('Jump index out of range: %d' % jp.index)
                elif jp.index >= steps:
                    logger.warning('Jump index exceed events range: %d/%d, ends current loop' % (jp.index, steps))
                    break
                else:
                    i = jp.index
                    if labeldict is None:
                        logger.debug('Jump at %d' % i)
                    continue
        return True
