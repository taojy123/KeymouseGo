from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any
from loguru import logger
import json5


class JsonObject:
    def __init__(self, content: Dict[str, Any]):
        self.content = content
        self.next_object = None
        self.next_object_if_false = None


class Parser(metaclass=ABCMeta):
    # Simply get json object
    @staticmethod
    @abstractmethod
    def parse(script_path: str, *args) -> JsonObject:
        pass


class ScriptParser(Parser):

    @staticmethod
    def parse(script_path: str, *args) -> JsonObject:
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

        objects: List[Dict[str, Any]] = content['scripts']

        label_maps: Dict[str, JsonObject] = {}
        pending_dict: Dict[JsonObject, str] = {}  # 如果对象要跳转到未收入的label，则暂存该对象等待遍历完成后(labelmaps完全更新)再添加内容

        head_object = ScriptParser.link_objects(objects, None, label_maps, pending_dict)
        if len(pending_dict) > 0:
            for json_object, target_label in pending_dict.items():
                target_object = label_maps.get(target_label, None)
                if target_object:
                    json_object.next_object = target_object
                else:
                    logger.error(f'Could not find label {target_label}')
        return head_object

    @staticmethod
    @logger.catch
    def link_objects(objects: List[Dict[str, Any]], target_object: JsonObject,
                     label_maps: Dict[str, JsonObject], pending_dict: Dict[JsonObject, str]) -> JsonObject:
        # 倒序遍历脚本，建立流程图
        objects.reverse()
        current_object: JsonObject = None
        for content in objects:
            content: Dict
            current_object = JsonObject(content)
            # 添加label映射
            if content.get('label', None) is not None:
                if label_maps.get(content['label'], None) is not None:
                    logger.warning(f'Overwrite label {content["label"]} to object {content}')
                label_maps[content['label']] = current_object

            object_type = content.get('type', None)
            if object_type in ['event', 'subroutine', 'custom']:
                # 直接连接
                current_object.next_object = target_object
            elif object_type == 'sequence':
                current_object.next_object = target_object
                current_object.content['events'] = \
                    ScriptParser.link_objects(content['events'], None, label_maps, pending_dict)
            elif object_type == 'if':
                # 涉及两个子序列的连接
                current_object.next_object = \
                    ScriptParser.link_objects(content['do'], target_object, label_maps, pending_dict)
                current_object.next_object_if_false = \
                    ScriptParser.link_objects(content['else'], target_object, label_maps, pending_dict)
            elif object_type == 'goto':
                if label_maps.get(content['tolabel'], None):
                    current_object.next_object = label_maps[content['tolabel']]
                else:
                    pending_dict[current_object] = content['tolabel']
            else:
                raise RuntimeError(f'Unexpected event type at {content}')
            target_object = current_object
        return current_object


class LegacyParser(Parser):

    @staticmethod
    def parse(script_path: str, *args) -> JsonObject:
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
        # 旧版脚本无流程控制，只需倒序遍历即可确定图
        content.reverse()
        target_object = None
        current_object = None
        for v in content:
            current_object = JsonObject({
                'delay': v[0],
                'event_type': v[1].upper(),
                'message': v[2].lower(),
                'action': v[3],
                'type': 'event'
            })
            current_object.next_object = target_object
            target_object = current_object
        return current_object
