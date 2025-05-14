# -*- encoding:utf-8 -*-
import datetime
from typing import List

import json5
import os
import sys
import threading
import platform
import locale
import Recorder

from PySide6.QtGui import QTextCursor
from qt_material import list_themes, QtStyleTools
from PySide6.QtCore import *
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide6.QtMultimedia import QSoundEffect
from loguru import logger

from Event import ScriptEvent, flag_multiplemonitor
from Plugin.Manager import PluginManager
from UIView import Ui_UIView

from KeymouseGo import to_abs_path
from Util.RunScriptClass import RunScriptClass
from Util.Global import State
from Util.ClickedLabel import Label


os.environ['QT_ENABLE_HIGHDPI_SCALING'] = "1"
# if platform.system() == 'Windows':
#     HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
#                 'XButton1', 'XButton2', 'Middle']
# else:
#     HOT_KEYS = ['F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
#                 'Middle']

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
    scripts = list(filter(lambda s: s.endswith('.txt') or s.endswith('.json5'), scripts))


def update_script_map():
    global scripts_map
    
    for (i, item) in enumerate(scripts):
        scripts_map[item] = i

class UIFunc(QMainWindow, Ui_UIView, QtStyleTools):
    updateStateSignal: Signal = Signal(State)

    def __init__(self, app):
        global scripts

        super(UIFunc, self).__init__()

        logger.info('assets root:{0}'.format(get_assets_path()))

        self.setupUi(self)

        self.app = app

        self.state = State(State.IDLE)

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

        PluginManager.reload()

        # Config
        self.choice_theme.addItems(['Default'])
        self.choice_theme.addItems(list_themes())
        # self.choice_theme.addItems(PluginManager.resources_paths)
        self.stimes.setValue(int(self.config.value("Config/LoopTimes")))
        self.mouse_move_interval_ms.setValue(int(self.config.value("Config/Precision")))
        self.choice_theme.setCurrentText(self.config.value("Config/Theme"))
        if self.config.value('Config/Script') is not None and self.config.value('Config/Script') in self.scripts:
            self.choice_script.setCurrentText(self.config.value('Config/Script'))
        self.stimes.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(self.onconfigchange)
        self.mouse_move_interval_ms.valueChanged.connect(Recorder.set_interval)
        self.choice_theme.currentTextChanged.connect(self.onchangetheme)
        self.choice_script.currentTextChanged.connect(self.onconfigchange)
        self.hotkey_stop.setText(self.config.value("Config/StopHotKey"))
        self.hotkey_start.setText(self.config.value("Config/StartHotKey"))
        self.hotkey_record.setText(self.config.value("Config/RecordHotKey"))


        self.onchangetheme()

        self.textlog.textChanged.connect(lambda: self.textlog.moveCursor(QTextCursor.End))

        # For tune playing
        self.player = QSoundEffect()
        self.volumeSlider.setValue(50)
        self.volumeSlider.valueChanged.connect(
            lambda: self.player.setVolume(
                self.volumeSlider.value()/100.0))

        self.record = []

        self.actioncount = 0

        # For better thread control
        self.runthread = None

        self.btrun.clicked.connect(self.OnBtrunButton)
        self.btrecord.clicked.connect(self.OnBtrecordButton)
        self.btpauserecord.clicked.connect(self.OnPauseRecordButton)
        self.bt_open_script_files.clicked.connect(self.OnBtOpenScriptFilesButton)
        self.choice_language.installEventFilter(self)
        self.choice_script.installEventFilter(self)
        self.btrun.installEventFilter(self)
        self.btrecord.installEventFilter(self)
        self.btpauserecord.installEventFilter(self)
        self.bt_open_script_files.installEventFilter(self)

        # 组合键缓冲池，[ctrl,shift,alt,cmd/start/win]可用作组合键，但不能单独用作启动热键
        self.keys_pool: List[str] = []
        self.hotkey_set_btn = None
        self.hotkey_stop.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_stop))
        self.hotkey_start.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_start))
        self.hotkey_record.clicked.connect(lambda: self.OnHotkeyButton(self.hotkey_record))

        # 热键引发状态转移
        def check_hotkeys(key_name):
            if key_name in Recorder.globals.key_combination_trigger:
                if self.state == State.SETTING_HOT_KEYS:
                    self.hotkey_set_btn.setText('+'.join(self.keys_pool))
                return False
            key_name = '+'.join([*self.keys_pool, key_name])

            if self.state == State.SETTING_HOT_KEYS:
                for btn in [self.hotkey_start, self.hotkey_record, self.hotkey_stop]:
                    if btn is not self.hotkey_set_btn and btn.text() != '' and btn.text() == key_name:
                        self.keys_pool.clear()
                        self.hotkey_set_btn.setText('')
                        self.update_state(State.IDLE)
                        return False
                self.hotkey_set_btn.setText(key_name)
                self.update_state(State.IDLE)
                self.onconfigchange()
                return False

            start_name = self.hotkey_start.text()
            stop_name = self.hotkey_stop.text()
            record_name = self.hotkey_record.text()

            if key_name == start_name:
                if self.state == State.IDLE:
                    logger.debug('{0} host start'.format(key_name))
                    self.OnBtrunButton()
                elif self.state == State.RUNNING:
                    logger.info('Script pause')
                    logger.debug('{0} host pause'.format(key_name))
                    self.runthread.set_pause()
                    self.update_state(State.PAUSE_RUNNING)
                elif self.state == State.PAUSE_RUNNING:
                    logger.info('Script resume')
                    self.runthread.resume()
                    logger.debug('{0} host resume'.format(key_name))
                    self.update_state(State.RUNNING)
            elif key_name == stop_name:
                if self.state == State.RUNNING or self.state == State.PAUSE_RUNNING:
                    logger.info('Script stop')
                    self.tnumrd.setText('broken')
                    self.runthread.resume()
                    logger.debug('{0} host stop'.format(key_name))
                    self.update_state(State.IDLE)
                elif self.state == State.RECORDING or self.state == State.PAUSE_RECORDING:
                    self.recordMethod()
                    logger.info('Record stop')
                    logger.debug('{0} host stop record'.format(key_name))
            elif key_name == record_name:
                if self.state == State.RECORDING:
                    self.pauseRecordMethod()
                    logger.debug('{0} host pause record'.format(key_name))
                elif self.state == State.PAUSE_RECORDING:
                    self.pauseRecordMethod()
                    logger.debug('{0} host resume record'.format(key_name))
                elif self.state == State.IDLE:
                    self.recordMethod()
                    logger.debug('{0} host start record'.format(key_name))
            return key_name in [start_name, stop_name, record_name]

        @Slot(ScriptEvent)
        def on_record_event(event: ScriptEvent):
            # 判断mouse热键
            if event.event_type == "EM":
                name = event.action_type
                if 'mouse x1 down' == name and check_hotkeys('xbutton1'):
                    return
                elif 'mouse x2 down' == name and check_hotkeys('xbutton2'):
                    return
                elif 'mouse middle down' == name and check_hotkeys('middle'):
                    return
            else:
                key_name = event.action[1].lower()
                if event.action_type == 'key down':
                    if key_name in Recorder.globals.key_combination_trigger and len(self.keys_pool) < 3 and key_name not in self.keys_pool:
                        self.keys_pool.append(key_name)
                    # listen for start/stop script
                    # start_name = 'f6'  # as default
                    # stop_name = 'f9'  # as default
                    check_hotkeys(key_name)
                elif event.action_type == 'key up':
                    if key_name in Recorder.globals.key_combination_trigger and key_name in self.keys_pool:
                        self.keys_pool.remove(key_name)
                        check_hotkeys(key_name)
                # 不录制热键
                for btn in [self.hotkey_start, self.hotkey_record, self.hotkey_stop]:
                    if key_name == btn.text():
                        return
            # 录制事件
            if self.state == State.RECORDING:
                if event.event_type == 'EM' and not flag_multiplemonitor:
                    tx, ty = event.action
                    event.action = ['{0}%'.format(tx), '{0}%'.format(ty)]
                event_dict = event.__dict__
                event_dict['type'] = 'event'
                # PluginManager.call_record(event_dict)
                self.record.append(event_dict)
                self.actioncount = self.actioncount + 1
                text = '%d actions recorded' % self.actioncount
                logger.debug('Recorded %s' % event)
                self.tnumrd.setText(text)
                self.textlog.append(str(event))
        logger.debug('Initialize at thread ' + str(QThread.currentThread()))
        Recorder.setuphook()
        Recorder.set_callback(on_record_event)
        Recorder.set_cursor_pose_change(self.cursor_pos_change)
        Recorder.set_interval(self.mouse_move_interval_ms.value())

    def eventFilter(self, watched, event: QEvent):
        et: QEvent.Type = event.type()
        # print(event, et)
        if et == QEvent.KeyPress or et == QEvent.KeyRelease:
            return True
        return super(UIFunc, self).eventFilter(watched, event)

    def onconfigchange(self):
        self.config.setValue("Config/LoopTimes", self.stimes.value())
        self.config.setValue("Config/Precision", self.mouse_move_interval_ms.value())
        self.config.setValue("Config/Theme", self.choice_theme.currentText())
        self.config.setValue("Config/Script", self.choice_script.currentText())
        self.config.setValue("Config/StartHotKey", self.hotkey_start.text())
        self.config.setValue("Config/StopHotKey", self.hotkey_stop.text())
        self.config.setValue("Config/RecordHotKey", self.hotkey_record.text())

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
        self.hotkey_stop.setText(self.config.value("Config/StopHotKey"))
        self.hotkey_start.setText(self.config.value("Config/StartHotKey"))
        self.hotkey_record.setText(self.config.value("Config/RecordHotKey"))

    def onchangetheme(self):
        theme = self.choice_theme.currentText()
        if theme == 'Default':
            self.apply_stylesheet(self.app, theme='default')
        else:
            self.apply_stylesheet(self.app, theme=theme)
        self.config.setValue("Config/Theme", self.choice_theme.currentText())

    @Slot(str)
    def playtune(self, filename: str):
        self.player.setSource(QUrl.fromLocalFile(get_assets_path('sounds', filename)))
        self.player.play()

    def closeEvent(self, event):
        self.config.sync()
        Recorder.dispose()
        if self.state == State.PAUSE_RUNNING:
            self.update_state(State.RUNNING)
        elif self.state == State.PAUSE_RECORDING:
            self.update_state(State.RECORDING)
        if self.runthread:
            self.runthread.resume()
        event.accept()

    def loadconfig(self):
        if not os.path.exists(to_abs_path('config.ini')):
            with open(to_abs_path('config.ini'), 'w', encoding='utf-8') as f:
                f.write('[Config]\n'
                        'StartHotKey=f6\n'
                        'StopHotKey=f9\n'
                        'RecordHotKey=f10\n'
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
        if self.state == State.PAUSE_RECORDING:
            logger.info('Record resume')
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Pause', None))
            self.update_state(State.RECORDING)
        elif self.state == State.RECORDING:
            logger.info('Record pause')
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Continue', None))
            self.tnumrd.setText('record paused')
            self.update_state(State.PAUSE_RECORDING)

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
        self.hotkey_start.setDisabled(True)
        self.hotkey_stop.setDisabled(True)
        self.hotkey_record.setDisabled(True)
        file_dialog.show()
        self.bt_open_script_files.setDisabled(False)
        self.btrecord.setDisabled(False)
        self.btrun.setDisabled(False)
        self.hotkey_start.setEnabled(True)
        self.hotkey_stop.setEnabled(True)
        self.hotkey_record.setEnabled(True)
        # 重新设置的为点击按钮时, 所处的位置
        self.choice_script.clear()
        self.choice_script.addItems(scripts)
        self.choice_script.setCurrentIndex(scripts_map['current_index'])

    def recordMethod(self):
        if self.state == State.RECORDING or self.state == State.PAUSE_RECORDING:
            logger.info('Record stop')
            with open(self.new_script_path(), 'w', encoding='utf-8') as f:
                json5.dump({"scripts": self.record}, indent=2, ensure_ascii=False, fp=f)
            self.btrecord.setText(QCoreApplication.translate("UIView", 'Record', None))
            self.tnumrd.setText('finished')
            self.record = []
            self.actioncount = 0
            self.choice_script.setCurrentIndex(0)
            self.btpauserecord.setText(QCoreApplication.translate("UIView", 'Pause Record', None))
            self.update_state(State.IDLE)
        elif self.state == State.IDLE:
            logger.info('Record start')
            self.textlog.clear()
            status = self.tnumrd.text()
            if 'running' in status or 'recorded' in status:
                return
            self.btrecord.setText(QCoreApplication.translate("UIView", 'Finish', None))
            self.tnumrd.setText('0 actions recorded')
            self.record = []
            self.update_state(State.RECORDING)

    def OnBtrecordButton(self):
        if self.state == State.RECORDING or self.state == State.PAUSE_RECORDING:
            self.record = self.record[:-2]
        self.recordMethod()

    def OnBtrunButton(self):
        logger.info('Script start')
        self.textlog.clear()
        self.update_state(State.RUNNING)
        if self.runthread:
            self.updateStateSignal.disconnect()
        self.runthread = RunScriptClass(self)
        self.runthread.start()

    def update_state(self, state):
        self.state = state
        if state != State.SETTING_HOT_KEYS or state != State.RECORDING or state != State.PAUSE_RECORDING:
            self.updateStateSignal.emit(self.state)
        if state == State.IDLE:
            self.hotkey_start.setEnabled(True)
            self.hotkey_stop.setEnabled(True)
            self.hotkey_record.setEnabled(True)
            self.btrun.setEnabled(True)
            self.btrecord.setEnabled(True)
            self.btpauserecord.setEnabled(False)
        elif state == State.RUNNING or state == State.PAUSE_RUNNING or state == State.SETTING_HOT_KEYS:
            self.hotkey_start.setEnabled(False)
            self.hotkey_stop.setEnabled(False)
            self.hotkey_record.setEnabled(False)
            self.btrun.setEnabled(False)
            self.btrecord.setEnabled(False)
            self.btpauserecord.setEnabled(False)
        elif state == State.RECORDING or state == State.PAUSE_RECORDING:
            self.hotkey_start.setEnabled(False)
            self.hotkey_stop.setEnabled(False)
            self.hotkey_record.setEnabled(False)
            self.btrun.setEnabled(False)
            self.btrecord.setEnabled(True)
            self.btpauserecord.setEnabled(True)

    def OnHotkeyButton(self, btn_obj: QObject):
        self.hotkey_set_btn = btn_obj
        self.update_state(State.SETTING_HOT_KEYS)

    @Slot(bool)
    def handle_runscript_status(self, succeed):
        self.update_state(State.IDLE)

    @Slot(tuple)
    def cursor_pos_change(self, pos):
        self.label_cursor_pos.setText(f'Cursor pos: {pos}')
