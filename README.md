```
 _______          _ ____            
 |__   __|        | |  _ \           
    | | ___   ___ | | |_) | _____  __
    | |/ _ \ / _ \| |  _ < / _ \ \/ /
    | | (_) | (_) | | |_) | (_) >  < 
    |_|\___/ \___/|_|____/ \___/_/\_\                       by bananalone
```

# 前言  
ToolBox是一个用于管理python脚本的CLI工具，采用插件式管理方式，功能包括对脚本安装、删除、装载、卸载，创建脚本模板，设置脚本运行参数以及运行所有装载的脚本。

# 架构
![architecture](./assets/architecture.jpg)  
- **Page** &nbsp;&nbsp; 显示界面类，包括换页（分支节点）和绑定事件函数（叶子节点）
- **core** &nbsp;&nbsp; 实现ToolBox的基本功能，包括设置插件运行参数、运行插件、插件管理以及创建插件模板
- **PluginsManager** &nbsp;&nbsp; 插件管理，包括列出所有已安装插件、获得所有已加载插件、安装、删除、装载和卸载
- **PluginsTable** &nbsp;&nbsp; 插件状态序列化

# 使用方法
```
python /path/to/src/main.py
```

# 界面

![homepage](./assets/homepage.jpg)  