import threading
import traceback

from PySide2.QtCore import QThread, Signal, QMutex, QWaitCondition, QDeadlineTimer
from PySide2.QtWidgets import QWidget
from loguru import logger
from Util.Parser import LegacyParser


mutex = QMutex()
cond = QWaitCondition()


class RunScriptClass(QThread):
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
                nointerrupt = nointerrupt and RunScriptClass.run_script_once(events, thd=self)
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
    @classmethod
    def run_script_once(cls, events, thd=None):
        steps = len(events)
        i = 0
        while i < steps:
            if thd:
                if thd.frame.isbrokenorfinish:
                    logger.info('Broken at [%d/%d]' % (i, steps))
                    return False
                thd.wait_if_pause()
                logger.trace(
                    '%s  [%d/%d %d/%d]' % (thd.running_text, i + 1, steps, thd.j + 1, thd.runtimes))
                thd.logSignal.emit('{0} [{1}/{2}]'.format(
                            events[i].summarystr(), i + 1, steps))
            event = events[i]
            event.execute(thd)
            i = i + 1
        return True
