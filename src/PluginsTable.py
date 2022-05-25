import os
import json

class PluginsTable:
    def load(self) -> dict:
        raise NotImplementedError
    
    def dump(self, plugins: dict):
        raise NotImplementedError


class JsonTable(PluginsTable):
    def __init__(self, path: str) -> None:
        if not os.path.isfile(path):
            with open(path, 'w') as f:
                f.write(r"{}")
        self.path = path
        
    def load(self) -> dict:
        with open(self.path, "r") as f:
            plugins = json.load(f)
        if isinstance(plugins, dict):
            return plugins
        return {}
        
    def dump(self, plugins: dict):
        if isinstance(plugins, dict):
            with open(self.path, 'w') as f:
                json.dump(plugins, f, indent=2)
