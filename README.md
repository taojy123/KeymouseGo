# KeymouseGo v2.2

功能：记录用户的鼠标键盘操作，通过触发按钮自动执行之前记录的操作，可设定执行的次数，可以理解为 `精简绿色版` 的 `按键精灵`。

用途：在进行某些操作简单、单调重复的工作时，使用本软件就可以很省力了。自己只要做一遍，然后接下来就让电脑来做。


----------------------

该软件通过 `Python` 语言编写，已编译为 `windows` 平台可执行文件，未安装 `Python` 的用户可直接下载 `release` 版本 https://github.com/taojy123/KeymouseGo/releases ，直接点击 `KeymouseGo.exe` 运行

<img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/sample.jpg" width="355">

----------------------

# 基本操作：

1、点击 `录制` 按钮，开始录制。

2、在计算机上进行任意操作，如点击鼠标、键盘输入，这部分的动作会被记录下来。

3、点击 `结束` 按钮，结束录制。

4、点击 `启动` 按钮，计算机会重复执行一遍第2步中所录制的动作。


# 提示：

1、可设置脚本重复执行的次数，如果为 `0` 即为无限循环。

2、默认启动热键为 `F6`，功能等同于 `启动` 按钮；默认终止热键为 `F9`，按下后将会停止正在运行的脚本。

3、录制时只记录鼠标点击动作和键盘动作，不记录鼠标移动轨迹。

4、每次录制结束后都会在 `scripts` 目前下生成一个新的脚本文件。

5、运行前可以在列表中选择一个需要执行的脚本。

6、`scripts` 下的脚本文件内容可以修改，修改时可参考如下所述 `脚本格式说明`。


# 脚本格式说明：

```
[
 [3000, "EM", "mouse left down", [100, 200]], 
 [50,   "EM", "mouse left up", [100, 200]], 
 [1000, "EK", "key down", "f"], 
 [50,   "EK", "key up", "f"], 
 [2000, "EM", "mouse right down", [300, 400]], 
 [50,   "EM", "mouse right up", [300, 400]]
]
```


每一行代表一次动作：
+ 每行的第 1 个元素表示时间间隔，指的是本次动作与上一次动作之间相隔的时间，单位为毫秒。
+ 每行的第 2 个元素表示鼠标动作或是键盘动作：`EM` 为鼠标，`EK` 为键盘。
+ 每行的第 3 个元素表示动作的类型：`mouse left down` 为鼠标左键按下，`mouse left up` 为鼠标左键抬起，`mouse right down` 为鼠标右键按下，`mouse right up` 为鼠标右键抬起，`key down` 键盘按键按下，`key up` 键盘按键抬起。
+ 每行的第 4 个元素表示具体的动作参数，当为鼠标动作时，由两个子元素构成，分别为鼠标所在的屏幕位置的横纵坐标；键盘动作时为按下或抬起的按键名称。
+ 修改时请严格遵守格式，否则可能导致脚本无法运行，建议修改前先备份一下。


综上所述，示例中的脚本运行后的效果为：
+ 开始运行 `3000ms` 后，在屏幕坐标 `(100,200)` 处 `按下鼠标左键`；
+ 等待 `50ms` 后在相同位置 `抬起鼠标左键`；
+ 等待 `1000ms` 后 `按下f键`；
+ 等待 `50ms` 后 `抬起f键`；
+ 等待 `2000ms` 后，在屏幕坐标 `(300,400)` 处 `按下鼠标左键`；
+ 等待 `50ms` 后在相同位置 `抬起鼠标左键`。


# 使用命令行运行：

直接运行指定脚本:
```
> KeymouseGo.exe scripts/0314_1452.txt
```

运行指定脚本3次:
```
> KeymouseGo.exe scripts/0314_1452.txt 3
```


# 设定屏幕缩放比例：

win10 系统的用户通常会修改屏幕的缩放比例，见下图

<img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/scale.png" width="386">

在修改了缩放比例后，录制的脚本时会出现坐标偏移的问题

具体参看此 issue: https://github.com/taojy123/KeymouseGo/issues/8

目前解决方案是，在 `屏幕缩放` 文本框中填写响应的值，比如 `125%`，然后再进行录制即可！



----------------------

# 赞赏支持

如果您觉得这个项目对您有所帮助，并乐意支持开源工作，可通过 `支付宝` 或 `微信支付` 为我赞赏支持

捐赠时可备注留下您的 `Github 主页地址`，我会将您加入 `感谢列表` 中（如果您愿意）

您的热情，我的动力！开源是一种精神，也是一种生活态度

<img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/donate.png" width="600">

感谢下列支持者:

<a href="https://github.com/liran319"><img src="https://avatars1.githubusercontent.com/u/4019372?s=50&v=4" height="50"></a>
<a href="https://github.com/WU731642061"><img src="https://avatars1.githubusercontent.com/u/30043630?s=50&v=4" height="50"></a>


感谢 JetBrains 免费提供开发工具

<a href="https://www.jetbrains.com/?from=KeymouseGo"><img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/jetbrains-variant-2.png" height="80"></a>

----------------------

# 已知的一些问题

`pynput` 在 `macOS` 上有兼容性问题，发现无法同时监听鼠标和键盘事件的时候。

经过简单的验证发现：
- 单纯的同时监听鼠标和键盘事件，没有问题
- 在 wxpython 中只监听鼠标事件，没有问题
- 在 wxpython 中只监听键盘事件，没有问题
- 在 wxpython 中同时监听键盘事件，有几率会报错，并无法正常监听键盘事件
- 暂时找不到解决方案，可能要考虑找 pynput 的替代品

详见此 issue https://github.com/moses-palmer/pynput/issues/55


----------------------

# 更新说明


暂时没法打包 `x86` 版本，32 位系统的同学请自行源码编译，或 [下载v1.5老版本](https://github.com/taojy123/KeymouseGo/releases/tag/v1.5) 使用


## v2.2
+ 优化了脚本格式，将动作时间间隔，放到每行脚本的首位，逻辑更加合理
+ 默认录制的第一个动作不加时间间隔，即按下启动按钮后立即执行第一个动作
+ 如果重复多次执行，可修改脚本中第一个动作的时间（单位毫秒）来决定每轮动作之间的相隔时间


## v2.1
+ 增加了屏幕缩放配置，兼容了修改过屏幕缩放比例的 win10 系统
+ 优化代码，兼容 `Python3`

## v2.0
+ 代码优化重构
+ 使用 `pynput` 实现动作捕捉和执行，不再需要安装 `pywin32` 和 `pyhook`
+ 兼容 macOS (需要在隐私设置中允许程序控制电脑)
+ `pynput` 似乎不兼容 WinXP，暂时没法打包 `x86` 版本

## v1.5
+ 修复自定义缩放后录制定位偏移 Bug

## v1.4
+ 增加命令行运行方式

## v1.3
+ Bug 修复

## v1.2
+ UI 更新
+ 移除了 `后台模式`
+ 简化了录制脚本，增强了可读性
+ 脚本文件名优化，可录制多个脚本，避免误操作覆盖了辛辛苦苦录制的脚本
+ 可自定义 `启动热键` 和 `终止热键`








