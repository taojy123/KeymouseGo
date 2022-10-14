# -*- encoding:utf-8 -*-
import datetime
import json5
import os
import sys
import threading
import platform
import locale
import Recorder

from PySide2.QtGui import QTextCursor
from qt_material import list_themes, QtStyleTools
from PySide2.QtCore import *
from PySide2.QtWidgets import QMainWindow, QApplication
from PySide2.QtMultimedia import QSoundEffect
from loguru import logger

from Event import ScriptEvent, flag_multiplemonitor
from UIView import Ui_UIView

from KeymouseGo import to_abs_path
from Util.RunScriptClass import RunScriptClass


os.environ['QT_ENABLE_HIGHDPI_SCALING'] = "1"
QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

if platform.system() == 'Windows':
    HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                'XButton1', 'XButton2', 'Middle']
else:
    HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
                'Middle']

logger.remove()
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
    scripts = list(filter(lambda s: s.endswith('.txt') or s.endswith('.json5'), scripts))


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

        self.choice_theme.addItems(['Default'])
        self.choice_theme.addItems(list_themes())
        self.choice_start.addItems(HOT_KEYS)
        self.choice_stop.addItems(HOT_KEYS)
        self.choice_record.addItems(HOT_KEYS)
        self.choice_start.setCurrentIndex(int(self.config.value("Config/StartHotKeyIndex")))
        self.choice_stop.setCurrentIndex(int(self.config.value("Config/StopHotKeyIndex")))
        self.choice_record.setCurrentIndex(int(self.config.value("Config/RecordHotKeyIndex")))
        self.stimes.setValue(int(self.config.value("Config/LoopTimes")))
        self.mouse_move_interval_ms.setValue(int(self.config.value("Config/Precision")))
        self.choice_theme.setCurrentText(self.config.value("Config/Theme"))
        if self.config.value('Config/Script') is not None and self.config.value('Config/Script') in self.scripts:
            self.choice_script.setCurrentText(self.config.value('Config/Script'))
        self.choice_start.currentIndexChanged.connect(self.onconfigchange)
        self.choice_stop.currentIndexChanged.connect(self.onconfigchange)
        self.choice_record.currentIndexChanged.connect(self.onconfigchange)
        self.stimes.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(Recorder.set_interval)
        self.choice_theme.currentTextChanged.connect(self.onchangetheme)
        self.choice_script.currentTextChanged.connect(self.onconfigchange)

        self.onchangetheme()

        self.textlog.textChanged.connect(lambda: self.textlog.moveCursor(QTextCursor.End))

        # For tune playing
        self.player = QSoundEffect()
        self.volumeSlider.setValue(100)
        self.volumeSlider.valueChanged.connect(lambda: self.player.setVolume(self.volumeSlider.value()/100.0))

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
            # 判断热键
            if event.event_type == 'EM':
                name = event.message
                if 'mouse x1 down' == name and hotkeymethod('xbutton1'):
                    return
                elif 'mouse x2 down' == name and hotkeymethod('xbutton2'):
                    return
                elif 'mouse middle down' and hotkeymethod('middle'):
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
            if not(not self.recording or self.running or self.pauserecord):
                if event.event_type == 'EM' and not flag_multiplemonitor:
                    tx, ty = event.action
                    event.action = ['{0}%'.format(tx), '{0}%'.format(ty)]
                self.record.append(event.__dict__)
                self.actioncount = self.actioncount + 1
                text = '%d actions recorded' % self.actioncount
                logger.debug('Recorded %s' % event)
                self.tnumrd.setText(text)
                self.textlog.append(str(event))
        logger.debug('Initialize at thread ' + str(threading.currentThread()))
        Recorder.setuphook()
        Recorder.set_callback(on_record_event)
        Recorder.set_interval(self.mouse_move_interval_ms.value())

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
        theme = self.choice_theme.currentText()
        if theme == 'Default':
            self.apply_stylesheet(self.app, theme='default')
        else:
            self.apply_stylesheet(self.app, theme=theme)
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
                        'Language=zh-cn\n'
                        'Theme=Default\n')
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
        script = '%s.json5' % now.strftime('%m%d_%H%M')
        if script in self.scripts:
            script = '%s.json5' % now.strftime('%m%d_%H%M%S')
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
            with open(self.new_script_path(), 'w', encoding='utf-8') as f:
                json5.dump({"scripts": self.record}, indent=2, ensure_ascii=False, fp=f)
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
