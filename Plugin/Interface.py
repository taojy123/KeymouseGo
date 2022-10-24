from abc import abstractmethod
from typing import Dict, List, Callable


class PluginMeta:
    def __init__(self, manifest: Dict):
        for key, value in manifest.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return f'{self.name}:{self.version}'


class PluginInterface:
    functions: List[Callable] = []

    def __init__(self, manifest: Dict):
        self.meta = PluginMeta(manifest)

    @abstractmethod
    def register_functions(self) -> Dict[str, Callable]:
        pass

    @abstractmethod
    def register_record_functions(self) -> List[Callable]:
        pass

