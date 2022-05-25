import os
import shutil

from PluginsTable import JsonTable, PluginsTable
from PluginsManager import PluginsManager

class Core:
    DESC = PluginsManager._DESC
    LOADED = PluginsManager._LOADED
    _PLUGIN_TEMPLATE_ROOT = 'plugin_template'
    
    def __init__(self, table: PluginsTable) -> None:
        self._table = table
        self._manager = PluginsManager(table.load())
        self._table.dump(self._manager.listPlugins())

    def createPluginTemplate(self, path: str):
        if os.path.exists(path):
            raise Exception("{} already exist".format(path))
        shutil.copytree(Core._PLUGIN_TEMPLATE_ROOT, path)

    def listPlugins(self) -> dict:
        return self._manager.listPlugins()

    def listLoadedPlugins(self) -> dict:
        plugins = self._manager.listPlugins()
        loadedPlugins = self._manager.listLoadedPlugins()
        rets = {}
        for name in loadedPlugins:
            rets[name] = plugins[name]
        return rets
    
    def install(self, path: str):
        self._manager.install(path)
        self._table.dump(self._manager.listPlugins())
        
    def uninstall(self, name: str):
        self._manager.uninstall(name)
        self._table.dump(self._manager.listPlugins())
        
    def load(self, name: str):
        self._manager.load(name)
        self._table.dump(self._manager.listPlugins())
        
    def unload(self, name: str):
        self._manager.unload(name)
        self._table.dump(self._manager.listPlugins())
        
    def setup(self, name: str):
        plugins = self._manager.listLoadedPlugins()
        if name not in plugins:
            raise Exception("{} not in loaded plugins".format(name))
        else:
            plugins[name].setup()

    def run(self, name: str) -> dict:
        plugins = self._manager.listLoadedPlugins()
        plugins[name].run()


_table = JsonTable(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins.json') )
core = Core(_table)