import os
import shutil
import importlib

class PluginsManager:
    # plugin attribute
    _DESC = "description"
    _LOADED = "loaded"
    
    # path
    _PLUGIN_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins') 
    
    def __init__(self, init_plugins: dict = {}) -> None:
        if not isinstance(init_plugins, dict):
            raise Exception("init plugins is not a dict")
        self.plugins = init_plugins # {name:{description: description massage, loaded: True or False}}
        self.loadedPlugins = {} # {name: instance}
        self._initManager()
        
    def listPlugins(self) -> dict:
        return self.plugins
    
    def listLoadedPlugins(self) -> dict:
        return self.loadedPlugins
    
    def install(self, path: str):
        if not os.path.isdir(path):
            raise Exception("{} is not a folder".format(path))
        if path.endswith('\\'):
            path = path[:-1]
        name = os.path.basename(path)
        if name in self.plugins:
            raise Exception("{} is already in plugins".format(name))
        shutil.copytree(path, os.path.join(PluginsManager._PLUGIN_ROOT, name))
        self._scanPlugin(name)
    
    def uninstall(self, name: str):
        if name in self.plugins:
            self.unload(name)
            del self.plugins[name]
        plugin_path = os.path.join(PluginsManager._PLUGIN_ROOT, name)
        if os.path.exists(plugin_path):
            shutil.rmtree(plugin_path)
    
    def load(self, name: str):
        if name not in self.plugins:
            raise Exception("{} is not installed".format(name))
        if name not in self.loadedPlugins:
            pluginPkg = '.'.join([os.path.basename(PluginsManager._PLUGIN_ROOT), name])
            try:
                PluginCls = importlib.import_module(".Plugin", package=pluginPkg).Plugin
                instance = PluginCls()
            except Exception:
                instance = None
            self.loadedPlugins[name] = {}
            self.loadedPlugins[name] = instance
            self.plugins[name][PluginsManager._LOADED] = True
    
    def unload(self, name: str):
        if name not in self.plugins:
            raise Exception("{} is not installed".format(name))
        if name in self.loadedPlugins:
            self.loadedPlugins[name] = None
            del self.loadedPlugins[name]
            self.plugins[name][PluginsManager._LOADED] = False
            
    def _initManager(self):
        plugins_in_folder = [plu for plu in os.listdir(PluginsManager._PLUGIN_ROOT) if not plu.startswith('_')]
        init_plugins = self.plugins
        self.plugins = {}
        self.loadedPlugins = {}
        for name in plugins_in_folder:
            if name in init_plugins:
                self.plugins[name] = init_plugins[name]
                if self.plugins[name][PluginsManager._LOADED]:
                    self.load(name)
            else:
                self._scanPlugin(name)
            
    def _scanPlugin(self, name):
        if name in self.plugins:
            return
        self.plugins[name] = {}
        self.plugins[name][PluginsManager._LOADED] = False
        plugin_path = os.path.join(PluginsManager._PLUGIN_ROOT, name)
        try:
            with open(os.path.join(plugin_path, PluginsManager._DESC + ".txt"), 'r') as f:
                desc = f.read()
        except:
            desc = ""
        self.plugins[name][PluginsManager._DESC] = desc
