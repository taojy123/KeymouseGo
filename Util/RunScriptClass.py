import threading
import traceback
from dataclasses import dataclass
from typing import List

from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition, QDeadlineTimer, Qt, Slot
from PySide6.QtWidgets import QWidget
from loguru import logger

from Util.Global import State
from Event import ScriptEvent
from Plugin.Manager import PluginManager
from Util.Parser import LegacyParser, ScriptParser, JsonObject

mutex = QMutex()
cond = QWaitCondition()


class RunScriptMeta:
    def pause(self):
        mutex.lock()
        cond.wait(mutex)
        mutex.unlock()

    def sleep(self, msecs: int):
        mutex.lock()
        cond.wait(mutex, QDeadlineTimer(int(msecs)))
        mutex.unlock()

    def resume(self):
        mutex.lock()
        cond.wakeAll()
        mutex.unlock()


class RunScriptClass(QThread, RunScriptMeta):
    logSignal: Signal = Signal(str)
    tnumrdSignal: Signal = Signal(str)
    btnSignal: Signal = Signal(bool)
    statusSignal: Signal = Signal(bool)
    playtuneSignal: Signal = Signal(str)

    def __init__(self, frame: QWidget):
        super().__init__()
        logger.debug('Thread created at thread' + str(threading.currentThread()))
        self.eventPause = False
        self.state = State.RUNNING
        self.script_path = frame.get_script_path()
        self.runtimes = frame.stimes.value()

        # 更新控件的槽函数
        self.logSignal.connect(frame.textlog.append)
        self.tnumrdSignal.connect(frame.tnumrd.setText)
        self.btnSignal.connect(frame.btrun.setEnabled)
        self.btnSignal.connect(frame.btrecord.setEnabled)
        frame.updateStateSignal.connect(self.update_state, Qt.DirectConnection)
        self.statusSignal.connect(frame.handle_runscript_status)
        self.playtuneSignal.connect(frame.playtune)

    def sleep(self, msecs: int):
        RunScriptMeta.sleep(self, msecs)

    def resume(self):
        self.eventPause = False
        super().resume()

    def set_pause(self):
        self.eventPause = True

    @Slot(State)
    def update_state(self, state):
        self.state = state

    def wait_if_pause(self):
        if self.eventPause:
            self.pause()
        else:
            self.resume()

    def run(self):
        logger.debug('Run script at thread' + str(QThread.currentThread()))

        if not self.script_path:
            self.tnumrdSignal.emit('script not found, please record first!')
            logger.warning('Script not found, please record first!')
            return

        self.btnSignal.emit(False)
        self.playtuneSignal.emit('start.wav')
        try:
            self.run_script_from_path(self.script_path)
        except Exception as e:
            logger.error(e)
            self.logSignal.emit('An error occurred during execution! Please check logs!')
        self.statusSignal.emit(True)
        self.playtuneSignal.emit('end.wav')

    @logger.catch
    def run_script_from_path(self, script_path: str):
        try:
            running_text = '%s running..' % script_path.split('/')[-1].split('\\')[-1]
            self.tnumrdSignal.emit(running_text)
            logger.info('%s running..' % script_path.split('/')[-1].split('\\')[-1])

            # 解析脚本，返回事件集合与扩展类对象
            logger.debug('Parse script..')
            try:
                head_object = ScriptParser.parse(script_path)
            except Exception as e:
                logger.warning('Failed to parse script, maybe it is using legacy grammar')
                try:
                    head_object = LegacyParser.parse(script_path)
                except Exception as e:
                    logger.error(e)
                    self.logSignal.emit('==============\nAn error occurred while parsing script')
                    self.logSignal.emit(str(e))
                    self.logSignal.emit('==============')

            j = 0
            nointerrupt = True
            logger.debug('Run script..')

            while (j < self.runtimes or self.runtimes == 0) and nointerrupt:
                logger.debug('===========%d==============' % j)
                if self.state == State.IDLE:
                    break
                self.tnumrdSignal.emit(f'{running_text}... Looptimes [{j + 1}/{self.runtimes}]')
                nointerrupt = nointerrupt and self.run_script_from_objects(head_object)
                j += 1
            if nointerrupt:
                self.tnumrdSignal.emit('finished')
                logger.info('Script run finish')
            else:
                logger.info('Script run interrupted')

        except Exception as e:
            logger.error('Run error: {0}'.format(e))
            traceback.print_exc()
            self.logSignal.emit('==============\nAn error occurred during runtime')
            self.logSignal.emit(str(e))
            self.logSignal.emit('==============')
            self.logSignal.emit('script run failed, please check your log file')
        finally:
            self.btnSignal.emit(True)

    # 执行集合中的ScriptEvent
    @logger.catch
    def run_script_from_objects(self, head_object: JsonObject, attach: List[str] = None):
        current_object = head_object
        while current_object is not None:
            self.wait_if_pause()
            if self.state == State.IDLE:
                return False
            if attach:
                PluginManager.call_group(attach, current_object)
            current_object = self.run_object(current_object)
        return True

    # Only return next object when 'goto' is indicated
    @logger.catch
    def run_object(self, json_object: JsonObject):
        object_type: str = json_object.content.get('type', None)
        call_group: List[str] = json_object.content.get('call', None)
        if call_group:
            PluginManager.call_group(call_group, json_object)
        if object_type == 'event':
            event = ScriptEvent(json_object.content)
            self.logSignal.emit(str(event))
            logger.debug(str(event))
            event.execute(self)
        elif object_type == 'sequence':
            self.run_script_from_objects(json_object.content['events'], json_object.content['attach'])
        elif object_type == 'if':
            result = PluginManager.call(json_object.content['judge'], json_object)
            if result:
                return json_object.next_object
            else:
                return json_object.next_object_if_false
        elif object_type == 'goto' or object_type == 'custom':
            pass
        elif object_type == 'subroutine':
            for path in json_object.content['path']:
                self.run_script_from_path(path)
        else:
            # Not supposed to happen
            logger.error(f'Unexpected event type when running {json_object.content}')
        return json_object.next_object


@dataclass
class StopFlag:
    value: bool


class RunScriptCMDClass(QThread, RunScriptMeta):
    def __init__(self, script_path: str, run_times: int, flag: StopFlag):
        super().__init__()
        self.script_path = script_path
        self.run_times = run_times
        self.flag = flag

    def sleep(self, msecs: int):
        RunScriptMeta.sleep(self, msecs)

    def run(self) -> None:
        self.run_script_from_path(self.script_path)

    @logger.catch
    def run_script_from_path(self, script_path):
        for path in script_path:
            logger.info('Script path:%s' % path)
            logger.debug('Parse script..')
            try:
                head_object = ScriptParser.parse(path)
            except Exception as e:
                logger.warning('Failed to parse script, maybe it is using legacy grammar')
                try:
                    head_object = LegacyParser.parse(path)
                except Exception as e:
                    logger.error(e)
            j = 0
            while j < self.run_times or self.run_times == 0:
                logger.info('===========%d==============' % j)
                self.run_script_from_objects(head_object)
                if self.flag.value:
                    logger.info('Stop Running thread')
                    break
                j += 1
            logger.info('%s run finish' % path)

    @logger.catch
    def run_script_from_objects(self, head_object: JsonObject, attach: List[str] = None):
        current_object = head_object
        while current_object is not None:
            if self.flag.value:
                break
            if attach:
                PluginManager.call_group(attach, current_object)
            current_object = self.run_object(current_object)

    @logger.catch
    def run_object(self, json_object: JsonObject):
        object_type: str = json_object.content.get('type', None)
        call_group: List[str] = json_object.content.get('call', None)
        if call_group:
            PluginManager.call_group(call_group, json_object)
        if object_type == 'event':
            event = ScriptEvent(json_object.content)
            logger.debug(str(event))
            event.execute(self)
        elif object_type == 'sequence':
            self.run_script_from_objects(json_object.content['events'], json_object.content['attach'])
        elif object_type == 'if':
            result = PluginManager.call(json_object.content['judge'], json_object)
            if result:
                return json_object.next_object
            else:
                return json_object.next_object_if_false
        elif object_type in ['goto', 'custom']:
            pass
        elif object_type == 'subroutine':
            self.run_script_from_path(json_object.content['path'])
        else:
            # Not supposed to happen
            logger.error(f'Unexpected event type when running {json_object.content}')
        return json_object.next_object

