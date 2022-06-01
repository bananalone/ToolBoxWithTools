```
 _______          _ ____            
 |__   __|        | |  _ \           
    | | ___   ___ | | |_) | _____  __
    | |/ _ \ / _ \| |  _ < / _ \ \/ /
    | | (_) | (_) | | |_) | (_) >  < 
    |_|\___/ \___/|_|____/ \___/_/\_\                       by bananalone
```

# 前言  
ToolBoxWithTools是包含了自用python工具的工具盒子，长期更新

纯净版ToolBox请前往 [https://github.com/bananalone/ToolBox](https://github.com/bananalone/ToolBox) 获取

# 现有工具
1. XorEncryption &nbsp;&nbsp; 使用异或运算对文件或者目录下的所有文件加密解密
2. OrganizeFiles &nbsp;&nbsp; 把文件夹里所有文件或子文件夹按照后缀进行分类整理，复制到新目录下，新目录不能存在
3. FuzzySearch &nbsp;&nbsp; 按照模式查找指定目录下的文件，采用编辑距离（莱温斯坦距离）模糊匹配
4. ImageToAscii &nbsp;&nbsp; 将图片转换为ASCII码，并保存为txt文件
5. TextToImage &nbsp;&nbsp; 将TXT文件里的文本转换为图片，字体为宋体，支持设置字体大小、字体颜色和背景颜色
6. AutoBot &nbsp;&nbsp; 按照脚本自动执行鼠标点击，键盘输入等操作

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