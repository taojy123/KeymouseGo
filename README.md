<div align="center">

# KeymouseGo

<br>
<img src="Preview.png" width="50%" height="50%" />

<div>
    <img alt="platform" src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blueviolet">
</div>
<div>
    <img alt="license" src="https://img.shields.io/github/license/taojy123/KeymouseGo">
    <img alt="language" src="https://img.shields.io/badge/python-%3E%3D%203.7-green">
    <img alt="stars" src="https://img.shields.io/github/stars/taojy123/KeymouseGo?style=social">
</div>
<div>
    <a href="https://deepwiki.com/taojy123/KeymouseGo">
        <img src="https://devin.ai/assets/deepwiki-badge.png" alt="Ask DeepWiki.com" height="20"/>
    </a>
</div>
<br>

[简体中文](README.md) | [English](README_en-US.md)

</div>

功能：记录用户的鼠标键盘操作，通过触发按钮自动执行之前记录的操作，可设定执行的次数，可以理解为 `精简绿色版` 的 `按键精灵`。

用途：在进行某些操作简单、单调重复的工作时，使用本软件就可以很省力了。自己只要做一遍，然后接下来就让电脑来做。


# 目录

+ [安装](#安装)
+ [使用方法](#使用方法)
  + [基本操作](#基本操作)
  + [提示](#提示)
  + [脚本语法说明](#脚本语法说明)
+ [关于作者](#关于作者)
+ [开源贡献者](#开源贡献者)

# 安装

该软件通过 `Python` 语言编写，已打包为可执行文件，未安装 `Python` 的用户可直接下载 [release](https://github.com/taojy123/KeymouseGo/releases) 版本 ，直接点击 `KeymouseGo` 运行

### 源码打包可执行文件

```
1. 安装 Python3
2. pip安装依赖
- (Windows) pip install -r requirements-windows.txt
- (Linux/MacOS) pip3 install -r requirements-universal.txt
3. pip安装pyinstaller
-  pip install pyinstaller
4. pyinstaller打包
- (Windows) pyinstaller -F -w --add-data "./assets;assets" KeymouseGo.py
- (Linux X11) pyinstaller -F -w --add-data "./assets:assets" --hidden-import "pynput.keyboard._xorg" --hidden-import "pynput.mouse._xorg" KeymouseGo.py
- (Linux Wayland) pyinstaller -F -w --add-data "./assets:assets"  --hidden-import "pynput.keyboard._uinput" --hidden-import "pynput.mouse._uinput" KeymouseGo.py
- (MacOS) pyinstaller -F -w --add-data "./assets:assets" --hidden-import "pynput.keyboard._darwin" --hidden-import "pynput.mouse._darwin" KeymouseGo.py
```

打包完成后，可执行文件在项目路径的`dist`文件夹内。

# 使用方法

## 基本操作

### 桌面模式

1、点击 `录制` 按钮，开始录制。

2、在计算机上进行任意操作，如点击鼠标、键盘输入，这部分的动作会被记录下来。

3、点击 `结束` 按钮，结束录制。

4、点击 `启动` 按钮，计算机会重复执行一遍第2步中所录制的动作。

### 命令行模式

直接运行指定脚本:
```
> ./KeymouseGo scripts/0314_1452.txt
```

运行指定脚本3次:
```
> ./KeymouseGo scripts/0314_1452.txt -rt 3
> ./KeymouseGo scripts/0314_1452.txt --runtimes 3
```

## 提示

1、可设置脚本重复执行的次数，如果为 `0` 即为无限循环。

2、默认启动热键为 `F6`，功能等同于 `启动` 按钮；默认终止热键为 `F9`，按下后将会停止正在运行的脚本。

3、录制时只记录鼠标点击动作和键盘动作，不记录鼠标移动轨迹。

4、每次录制结束后都会在 `scripts` 目前下生成一个新的脚本文件。

5、运行前可以在列表中选择一个需要执行的脚本。

6、`scripts` 下的脚本文件内容可以修改，修改时可参考如下所述 `脚本格式说明`。

7、热键设置中的`Middle`指代鼠标中键，`XButton`指代鼠标侧键

8、由于程序速度受限，当输入的鼠标速度大于一定值时脚本将无法以预期的输入速度执行

9、部分系统环境中，可能出现无法录制完整的鼠标事件的情况，请以管理员身份/root身份运行此工具即可正常使用。

10、使用Mac的用户，需要确保程序在辅助功能白名单，如果使用打包的exec文件，则还需要确保终端也在辅助功能白名单。 如果app程序闪退，请尝试给予`~/.qt_material`目录下文件的写权限:
```bash
chmod -R 770 ~/.qt_material
```

11、对于Linux/Mac用户，如果在以管理员身份运行后仍然存在无法录制或执行的问题，可以参考[pynput的文档](https://pynput.readthedocs.io/en/latest/limitations.html)

## 脚本语法说明
> 演示屏幕分辨率为`1920 * 1080`

脚本为 `json5` 格式，每个最内层的jsonobject代表一个事件
```json5
{
  scripts: [
    // 开始运行 `3000ms` 后，在屏幕相对坐标 `(0.05208, 0.1852)`即 `(100,200)` 处 `按下鼠标右键`；
    {type: "event", event_type: "EM", delay: 3000, action_type: "mouse right down", action: ["0.05208%", "0.1852%"]},
    // 等待 `50ms` 后在相同位置 `抬起鼠标右键`；
    // 横纵坐标为[-1, -1]时，表示在鼠标当前所在位置执行操作。
    {type: "event", event_type: "EM", delay: 50, action_type: "mouse right up", action: [-1, -1]},
    // 等待 `1000ms` 后 `按下f键`；
    {type: "event", event_type: "EK", delay: 1000, action_type: "key down", action: [70, 'F', 0]},
    // 等待 `50ms` 后 `抬起f键`；
    {type: "event", event_type: "EK", delay: 50, action_type: "key up", action: [70, 'F', 0]},
    // 等待 `100ms` 后，在屏幕相对坐标 `(0.2604, 0.4630)`即 `(500, 500)` 处 `按下鼠标左键`；
    {type: "event", event_type: "EM", delay: 100, action_type: "mouse left down", action: ["0.2604%", "0.4630%"]},
    // 等待 `100ms` 后，鼠标移动至相对坐标 `(0.2604, 0.5556)`即 `(500, 600)` 位置；
    {type: "event", event_type: "EM", delay: 100, action_type: "mouse move", action: ["0.2604%", "0.5556%"]},
    // 等待 `100ms` 后，在屏幕相对坐标 `(0.3125, 0.5556)`即 `(600, 600)` 处 `抬起鼠标左键`；
    {type: "event", event_type: "EM", delay: 100, action_type: "mouse left up", action: ["0.3125%", "0.5556%"]},
    // 等待 `100ms` 后，在当前位置输入 `你好 world` 文字。
    {type: "event", event_type: "EX", delay: 100, action_type: "input", action: "你好 world"}
  ]
}
```


## 高级功能

功能的使用详见[wiki](https://github.com/taojy123/KeymouseGo/wiki/文档#脚本语法)


# 关于作者

我是陶佳元，热爱代码，怀旧，在互联网上常用的 ID 有 taojy123 、tao.py。

我的个人站点 [tslow.cn](https://tslow.cn) 整理并罗列了一些 `个人项目` 和 `小工具` 合集。

你可以在 [简书](http://jianshu.tslow.cn) 浏览我最新发布的文章，还可以在 [B站](https://space.bilibili.com/145137942) 观看我的技术分享和生活纪实。

我的邮箱: taojy123@163.com

----------------------

# 开源贡献者

[![Contributors](https://contrib.rocks/image?repo=taojy123/keymousego)](https://github.com/taojy123/keymousego/graphs/contributors)

如果您是开发爱好者，并对本项目感兴趣，欢迎参与项目的共同建设，您可以通过本项目的[**dev**](https://github.com/taojy123/KeymouseGo/tree/dev)分支查看目前的进度，并且可以向本项目的[**dev**](https://github.com/taojy123/KeymouseGo/tree/dev)分支提交 Pull request 来贡献代码。

感谢 JetBrains 免费提供开发工具

<a href="https://www.jetbrains.com/?from=KeymouseGo"><img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/jetbrains-variant-2.png" height="80"></a>
