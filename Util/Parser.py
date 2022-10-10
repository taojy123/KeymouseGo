from abc import ABCMeta, abstractmethod
from typing import List
from Event import ScriptEvent
from loguru import logger
import json5


class ScriptParser(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def parse(script_path: str, *args) -> List[ScriptEvent]:
        pass


class LegacyParser(ScriptParser):

    @staticmethod
    def parse(script_path: str, *args) -> List[ScriptEvent]:
        logger.info('Use Legacy Parser')

        try:
            content = json5.load(open(script_path, 'r', encoding='utf8'))
        except Exception as e:
            logger.warning(e)
            try:
                content =  json5.load(open(script_path, 'r', encoding='gbk'))
            except Exception as e:
                logger.error(e)

        logger.debug('Script content')
        logger.debug(content)
        # Wrapped as ScriptEvent
        events = []
        for _, v in enumerate(content):
            delay = v[0]
            event_type = v[1].upper()
            message = v[2].lower()
            action = v[3]
            events.append(ScriptEvent({
                'delay': delay,
                'event_type': event_type,
                'message': message,
                'action': action
            }))
        return events
