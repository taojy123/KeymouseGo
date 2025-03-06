import os
import sys
from typing import Dict, Callable, List, Any
from loguru import logger
from Plugin.Interface import PluginInterface
from Util.Parser import JsonObject
from importlib.machinery import SourceFileLoader
import json5


def to_abs_path(*args):
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                        *args)


class PluginManager:
    functions: Dict[str, Callable] = {}
    # record_functions: List[Callable] = []
    plugins: List[PluginInterface] = []
    resources_paths: List[str] = []


    @staticmethod
    def load_manifest(path: str) -> Dict:
        manifest = None
        manifest_path = os.path.join(path, 'manifest.json5')
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json5.load(f)
        return manifest

    # 在目录plugins下搜寻启用的有效插件，同时生成实例
    @staticmethod
    @logger.catch
    def discover_plugin():
        if not os.path.exists(to_abs_path('plugins')):
            os.mkdir(to_abs_path('plugins'))
        with os.scandir(to_abs_path('plugins')) as it:
            for entry in it:
                entry: os.DirEntry
                if entry.is_dir():
                    manifest = PluginManager.load_manifest(entry.path)
                    if manifest and manifest['enabled']:
                        if entry.path not in sys.path:
                            sys.path.append(entry.path)
                        if manifest.get('entry', None) is not None and manifest.get('plugin_class', None) is not None:
                            loader = SourceFileLoader(manifest['plugin_class'], os.path.join(entry.path, manifest["entry"]))
                            plugin_module = loader.load_module()
                            plugin_class = getattr(plugin_module, manifest['plugin_class'])
                            PluginManager.plugins.append(plugin_class(manifest))
                        if manifest.get('resources_path') is not None:
                            for path in manifest['resources_path']['theme']:
                                PluginManager.resources_paths.append(os.path.join(entry.path, path))

        logger.info(f'Discovered Plugin {[plugin_ins.meta.name for plugin_ins in PluginManager.plugins]}')

    # 调用实例的注册方法
    @staticmethod
    @logger.catch
    def register_plugin():
        for plugin_ins in PluginManager.plugins:
            funcs = plugin_ins.register_functions()
            # funcs_rec = plugin_ins.register_record_functions()
            if funcs:
                PluginManager.functions.update(funcs)
            # if funcs_rec:
            #     PluginManager.record_functions.extend(funcs_rec)
        logger.info(f'Registered functions: {PluginManager.functions.keys()}')
        # logger.info(f'Registered record functions: {PluginManager.record_functions}')
        logger.info(f'Additional Resources: {PluginManager.resources_paths}')

    @staticmethod
    @logger.catch
    def call(function_name: str, json_object: JsonObject):
        func = PluginManager.functions.get(function_name, None)
        if func:
            return func(json_object)
        else:
            logger.warning(f'Cannot find function {function_name} in registered plugins')
            return None

    @staticmethod
    def call_group(function_group: List[str], json_object: JsonObject):
        for function_name in function_group:
            PluginManager.call(function_name, json_object)

    # @staticmethod
    # def call_record(event: Dict[str, Any]):
    #     for functions in PluginManager.record_functions:
    #         functions(event)

    @staticmethod
    def reload():
        # 暂时采用全部重新加载的方案
        PluginManager.functions = {}
        PluginManager.record_functions = []
        PluginManager.plugins = []
        PluginManager.resources_paths = []
        PluginManager.discover_plugin()
        PluginManager.register_plugin()
