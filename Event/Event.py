import time
from abc import ABCMeta, abstractmethod


class Event(metaclass=ABCMeta):
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

    def summarystr(self):
        if self.event_type == 'EK':
            return 'key {0} {1} after {1}ms'.format(self.action[1], self.message[4:], self.delay)
        else:
            return '{0} after {1}ms'.format(self.message, self.delay)

    # 延时
    def sleep(self, thd=None):
        if thd:
            thd.sleep(self.delay)
        else:
            time.sleep(self.delay / 1000.0)

    @abstractmethod
    def execute(self, thd=None):
        pass
