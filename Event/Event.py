from abc import ABCMeta, abstractmethod
from typing import Dict, Any


class Event(metaclass=ABCMeta):
    # 传入字典进行初始化
    def __init__(self, content: Dict[str, Any]):
        """Default param: delay, event_type, message, action"""
        for key in ['delay', 'event_type', 'action_type', 'action']:
            setattr(self, key, content[key])

    def __str__(self):
        if self.event_type == 'EK':
            return 'key {0} {1} after {2}ms'.format(self.action[1], self.action_type[4:], self.delay)
        elif self.event_type == 'EM':
            return '{0} at {2} after {1}ms'.format(self.action_type, self.delay, self.action)
        else:
            return str(self.__dict__)

    # 延时
    def sleep(self, thd):
        thd.sleep(self.delay)

    @abstractmethod
    def execute(self, thd=None):
        pass
