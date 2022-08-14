# 开发中可能遇到的坑


### 解决安装了 wxpython 后依旧无法 import wx 的问题

C:\Python37\Lib\site-packages\
添加 wx.pth 文件 内容
wx-3.0-msw


--------



### import win32api 报错 DLL load failed

尝试安装 exe 版本的 pywin32 安装包

--------

### 解决 Boa-constructor 双击后无法打开问题

修改 wx 模块的 __init__.py 文件 (路径一般为 C:\Python37\Lib\site-packages\wx-3.0-msw\___init__.py ), 末尾添加一行:
NO_3D = 0


--------



### 解决 boa-constructor 0.6.1 运行源代码面板中空白一片

在boa根目录，找到 Palette.py，将 408行的语句 　　　　newButton = btnType(self, mID, None, wx.Point(self.posX, self.posY), 修改为 　　　　newButton = btnType(self, mID, None, wx.Point(self.posX, 0),
就可以正常使用了

参考：http://blog.csdn.net/rickleo/article/details/6532595


--------



