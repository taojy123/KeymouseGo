import time
from abc import ABCMeta, abstractmethod
from typing import Dict, Any


class Event(metaclass=ABCMeta):
    # 传入字典进行初始化
    def __init__(self, content: Dict[str, Any]):
        """Default param: delay, event_type, message, action"""
        for key, value in content.items():
            setattr(self, key, value)

    def __str__(self):
        if self.event_type == 'EK':
            return 'key {0} {1} after {2}ms'.format(self.action[1], self.message[4:], self.delay)
        else:
            return '{0} at {2} after {1}ms'.format(self.message, self.delay, self.action)

    # 延时
    def sleep(self, thd=None):
        if thd:
            thd.sleep(self.delay)
        else:
            time.sleep(self.delay / 1000.0)

    @abstractmethod
    def execute(self, thd=None):
        pass
