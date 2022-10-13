import threading
import traceback
from dataclasses import dataclass

from PySide2.QtCore import QThread, Signal, QMutex, QWaitCondition, QDeadlineTimer
from PySide2.QtWidgets import QWidget
from loguru import logger
from Util.Parser import LegacyParser, ScriptParser

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
    logSignal = Signal(str)
    tnumrdSignal = Signal(str)
    btnSignal = Signal(bool)

    def __init__(self, frame: QWidget):
        super().__init__()
        logger.debug('Thread created at thread' + str(threading.currentThread()))
        self.frame = frame
        self.eventPause = False

        # 更新控件的槽函数
        self.logSignal.connect(frame.textlog.append)
        self.tnumrdSignal.connect(frame.tnumrd.setText)
        self.btnSignal.connect(frame.btrun.setEnabled)
        self.btnSignal.connect(frame.btrecord.setEnabled)

    def sleep(self, msecs: int):
        RunScriptMeta.sleep(self, msecs)

    def resume(self):
        self.eventPause = False
        super().resume()

    def wait_if_pause(self):
        if self.eventPause:
            self.pause()
        else:
            self.resume()

    @logger.catch
    def run(self):
        logger.debug('Run script at thread' + str(threading.currentThread()))
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
                events = ScriptParser.parse(script_path)
            except Exception as e:
                logger.warning('Failed to parse script, maybe it is using legacy grammar')
                try:
                    events = LegacyParser.parse(script_path)
                except Exception as e:
                    logger.error(e)
                    self.logSignal.emit('==============\nAn error occurred while parsing script')
                    self.logSignal.emit(str(e))
                    self.logSignal.emit('==============')

            self.j = 0
            nointerrupt = True
            logger.debug('Run script..')
            self.frame.playtune('start.wav')
            self.runtimes = self.frame.stimes.value()
            while (self.j < self.runtimes or self.runtimes == 0) and nointerrupt:
                logger.debug('===========%d==============' % self.j)
                current_status = self.frame.tnumrd.text()
                if current_status in ['broken', 'finished']:
                    self.frame.running = False
                    break
                self.tnumrdSignal.emit('{0}... Looptimes [{1}/{2}]'.format(
                    self.running_text, self.j + 1, self.runtimes))
                nointerrupt = nointerrupt and self.run_script_once(events)
                self.j += 1
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

    # 执行集合中的ScriptEvent
    def run_script_once(self, events):
        steps = len(events)
        i = 0
        while i < steps:
            self.wait_if_pause()
            if self.frame.is_broken_or_finish:
                logger.info('Broken at [%d/%d]' % (i, steps))
                return False
            logger.trace(
                '%s  [%d/%d %d/%d]' % (self.running_text, i + 1, steps, self.j + 1, self.runtimes))
            self.logSignal.emit('{0} [{1}/{2}]'.format(
                        events[i], i + 1, steps))
            event = events[i]
            logger.debug(event)
            event.execute(self)
            i = i + 1
        return True


@dataclass
class StopFlag:
    flag: bool


class RunScriptCMDClass(QThread, RunScriptMeta):
    def __init__(self, script_path: str, run_times: int, flag: StopFlag):
        super().__init__()
        self.script_path = script_path
        self.run_times = run_times
        self.flag = flag

    def sleep(self, msecs: int):
        RunScriptMeta.sleep(self, msecs)

    def run(self) -> None:
        try:
            for path in self.script_path:
                logger.info('Script path:%s' % path)
                logger.debug('Parse script..')
                try:
                    events = ScriptParser.parse(path)
                except Exception as e:
                    logger.warning('Failed to parse script, maybe it is using legacy grammar')
                    try:
                        events = LegacyParser.parse(path)
                    except Exception as e:
                        logger.error(e)
                j = 0
                while j < self.run_times or self.run_times == 0:
                    logger.info('===========%d==============' % j)
                    steps = len(events)
                    i = 0
                    while i < steps:
                        event = events[i]
                        if self.flag.flag:
                            break
                        event.execute(self)
                        logger.debug(event)
                        i = i + 1
                    if self.flag.flag:
                        logger.info('Stop Running thread')
                        break
                    j += 1
                logger.info('%s run finish' % path)
        except Exception as e:
            logger.error(e)
            raise e
