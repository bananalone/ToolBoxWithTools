import os

from core import core
from Page import Page

class App:
    _CLEAR = "cls" if os.name == 'nt' else 'clear'
    
    def __init__(self) -> None:
        self.homepage = None
        self.listToolsPage = None
        self.listLoadedToolsPage = None
        self.currentPage = None
        self._setPlugins = {}
        self._init_pages()
        
    def run(self):
        hello = '''
  _______          _ ____            
 |__   __|        | |  _ \           
    | | ___   ___ | | |_) | _____  __
    | |/ _ \ / _ \| |  _ < / _ \ \/ /
    | | (_) | (_) | | |_) | (_) >  < 
    |_|\___/ \___/|_|____/ \___/_/\_\                          
        
        '''
        while self.currentPage:
            os.system(App._CLEAR)
            if not self.currentPage.isLeaf():
                print(hello)
            self.currentPage = self.currentPage.next()
            
    def _init_pages(self):
        self.homepage = Page("Home", "Tool core is a collection of useful python tools").setParentItem(None)
        self.listToolsPage = Page("ListTools", "List all python tools").setParentItem(self.homepage)
        self.listLoadedToolsPage = Page("ListLoadedTools", "List loaded python tools").setParentItem(self.homepage)
        runPage = Page("RunLoadedTools", "Run all loaded python tools", func=self._run_event).setParentItem(self.homepage)
        installPage = Page("InstallTool", "Install python tools", func=self._install_event).setParentItem(self.homepage)
        createTemplatePage = Page("CreateTool", "Create your own python tool", func=self._createTemplate_event).setParentItem(self.homepage)
        self.homepage.setChildrenItems(self.listToolsPage, self.listLoadedToolsPage, runPage, installPage, createTemplatePage)
        self.currentPage = self.homepage
        loadedPlugins = core.listLoadedPlugins()
        for name in loadedPlugins:
            self._setPlugins[name] = False
        self._refresh()
    
    def _uninstall_event(self, name):
        def inner():
            core.uninstall(name)
            self._refresh()
            print("Uninstalled {} successfully".format(name))
        return inner
    
    def _load_event(self, name):
        def inner():
            core.load(name)
            self._setPlugins[name] = False
            self._refresh()
            print("Load {} successfully".format(name))
        return inner
    
    def _unload_event(self, name):
        def inner():
            core.unload(name)
            self._refresh()
            print("Unload {} successfully".format(name))
        return inner

    def _setup_event(self, name):
        def inner():
            core.setup(name)
            self._setPlugins[name] = True
            self._refresh()
            print("\nSetup {} successfully".format(name))
        return inner

    def _run_event(self):
        loadedPlugins = core.listLoadedPlugins()
        for name in loadedPlugins:
            print(">>> Start run {} <<<\n".format(name))
            core.run(name)
            print("\n>>> {} finished <<<1".format(name))
            
    def _install_event(self):
        path = input("Enter path of the plugin >>> ")
        core.install(path)
        self._refresh()
        print("Installed successfully")
        
    def _createTemplate_event(self):
        path = input("Enter where to create the plugin template >>> ")
        core.createPluginTemplate(path)
        
    def _gen_tool_pages(self, parent, plugins: dict) -> list:
        pages = []
        for name in plugins:
            itemName = "{name}{loaded}".format(name=name, loaded="(Loaded)" if plugins[name][core.LOADED] else "")
            pluginPage = Page(itemName, plugins[name][core.DESC]).setParentItem(parent)
            loadPage = Page("Load", "Load python tool", func=self._load_event(name)).setParentItem(pluginPage)
            unloadPage = Page("Unload", "Unload python tool", func=self._unload_event(name)).setParentItem(pluginPage)
            uninstallPage = Page("Uninstall", "Uninstall python tool", func=self._uninstall_event(name)).setParentItem(pluginPage)
            pluginPage.setChildrenItems(loadPage, unloadPage, uninstallPage)
            pages.append(pluginPage)
        return pages

    def _gen_loaded_tool_pages(self, parent, plugins: dict) -> list:
        pages = []
        for name in plugins:
            itemName = "{name}{iSet}".format(name=name, iSet="(Set)" if self._setPlugins[name] else "")
            pluginPage = Page(itemName, plugins[name][core.DESC]).setParentItem(parent)
            setupPage = Page("Setup", "Setup python tool", func=self._setup_event(name)).setParentItem(pluginPage)
            pluginPage.setChildrenItems(setupPage)
            pages.append(pluginPage)
        return pages

    def _refresh(self):
        toolPages = self._gen_tool_pages(self.listToolsPage, core.listPlugins())
        self.listToolsPage.setParentItem(self.homepage).setChildrenItems(*toolPages)
        loadedToolPages = self._gen_loaded_tool_pages(self.listLoadedToolsPage, core.listLoadedPlugins())
        self.listLoadedToolsPage.setParentItem(self.homepage).setChildrenItems(*loadedToolPages)
