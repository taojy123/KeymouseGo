from abc import ABCMeta, abstractmethod
from typing import List, Dict
from Event import ScriptEvent
from loguru import logger
import json5


class Parser(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def parse(script_path: str, *args) -> List[ScriptEvent]:
        pass


class ScriptParser(Parser):

    @staticmethod
    def parse(script_path: str, *args) -> List[ScriptEvent]:
        logger.info('Use Script Parser')

        try:
            with open(script_path, 'r', encoding='utf8') as f:
                content: Dict = json5.load(f)
        except Exception as e:
            logger.warning(e)
            try:
                with open(script_path, 'r', encoding='gbk') as f:
                    content: Dict = json5.load(f)
            except Exception as e:
                logger.error(e)

        logger.debug('Script content')
        logger.debug(content)

        # TODO: Link to plugin manager
        plugin = None
        if content.get('plugin') is not None:
            plugin = content['plugin']

        scripts = content['scripts']
        # Wrapped as ScriptEvent
        events = []
        for i, v in enumerate(scripts):
            events.append(ScriptEvent(v))
        return events


class LegacyParser(Parser):

    @staticmethod
    def parse(script_path: str, *args) -> List[ScriptEvent]:
        logger.info('Use Legacy Parser')

        try:
            with open(script_path, 'r', encoding='utf8') as f:
                content = json5.load(f)
        except Exception as e:
            logger.warning(e)
            try:
                with open(script_path, 'r', encoding='gbk') as f:
                    content = json5.load(f)
            except Exception as e:
                logger.error(e)

        logger.debug('Script content')
        logger.debug(content)
        # Wrapped as ScriptEvent
        events = []
        for _, v in enumerate(content):
            events.append(ScriptEvent({
                'delay': v[0],
                'event_type': v[1].upper(),
                'message': v[2].lower(),
                'action': v[3]
            }))
        return events
