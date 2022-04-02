# KeymouseGo v3.2.2

功能：记录用户的鼠标键盘操作，通过触发按钮自动执行之前记录的操作，可设定执行的次数，可以理解为 `精简绿色版` 的 `按键精灵`。

用途：在进行某些操作简单、单调重复的工作时，使用本软件就可以很省力了。自己只要做一遍，然后接下来就让电脑来做。

----------------------

该软件通过 `Python` 语言编写，已编译为 `windows` 平台可执行文件，未安装 `Python` 的用户可直接下载 `release` 版本 https://github.com/taojy123/KeymouseGo/releases ，直接点击 `KeymouseGo.exe` 运行

<img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/sample.jpg" width="355">

----------------------


# 关于作者：

我是陶佳元，热爱代码，怀旧，在互联网上常用的 ID 有 taojy123 、tao.py。

我的个人站点 [tslow.cn](https://tslow.cn) 整理并罗列了一些 `个人项目` 和 `小工具` 合集。

你可以在 [简书](http://jianshu.tslow.cn) 浏览我最新发布的文章，还可以在 [B站](https://space.bilibili.com/145137942) 观看我的技术分享和生活纪实。

我的邮箱: taojy123@163.com

----------------------

# 开源贡献者:

如果您是开发爱好者，并对本项目感兴趣，欢迎参与项目的共同建设，您可以向本项目提交 Pull request 来贡献代码。

在此，特别感谢积极贡献者：

<a href="https://github.com/Monomux"><img src="https://avatars.githubusercontent.com/u/70839036?s=80&v=4" height="80"></a>
  
Monomux

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


部分系统环境中，可能出现无法录制完整的鼠标事件的情况，请以管理员身份运行此工具即可正常使用。


# 脚本语法说明：
> 演示屏幕分辨率为`1920 * 1080`

```
[
 [3000, "EM", "mouse right down", [0.052083333333333336, 0.18518518518518517]],    // 开始运行 `3000ms` 后，在屏幕相对坐标 `(0.052083333333333336, 0.18518518518518517)`即 `(100,200)` 处 `按下鼠标右键`；
 [50,   "EM", "mouse right up",   [0.052083333333333336, 0.18518518518518517]],    // 等待 `50ms` 后在相同位置 `抬起鼠标右键`；
 [1000, "EK", "key down",         (70, 'F', 0)],                                   // 等待 `1000ms` 后 `按下f键`；
 [50,   "EK", "key up",           (70, 'F', 0)],                                   // 等待 `50ms` 后 `抬起f键`；
 [100,  "EM", "mouse left down",  [0.2604166666666667, 0.46296296296296297]],      // 等待 `100ms` 后，在屏幕相对坐标 `(0.2604166666666667, 0.46296296296296297)`即 `(500, 500)` 处 `按下鼠标左键`；
 [100,  "EM", "mouse move",       [0.2604166666666667, 0.5555555555555556]],       // 等待 `100ms` 后，鼠标移动至相对坐标 `(0.2604166666666667, 0.5555555555555556)`即 `(500, 600)` 位置；
 [100,  "EM", "mouse left down",  [0.3125, 0.5555555555555556]],                   // 等待 `100ms` 后，在屏幕相对坐标 `(0.3125, 0.5555555555555556)`即 `(600, 600)` 处 `抬起鼠标左键`；
 [100,  "EX", "input",            "你好 world"],                                   // 等待 `100ms` 后，在当前位置输入 `你好 world` 文字。
]
```

脚本为 `json` 格式，每一行代表一次动作：
+ 每行的第 1 个元素表示时间间隔，指的是本次动作与上一次动作之间相隔的时间，单位为毫秒。
+ 每行的第 2 个元素表示鼠标动作或是键盘动作：`EM` 为鼠标，`EK` 为键盘，`EX` 为其他拓展动作。
+ 每行的第 3 个元素表示动作的类型：
  + `mouse left down` 为鼠标左键按下，`mouse left up` 为鼠标左键抬起，
  + `mouse right down` 为鼠标右键按下，`mouse right up` 为鼠标右键抬起，
  + `mouse middle down` 为鼠标中键按下， `mouse middle up` 为鼠标中键抬起，
  + `mouse wheel up` 为鼠标滚轮上滑， `mouse wheel down` 为鼠标滚轮下滑，
  + `key down` 为键盘按键按下，`key up` 为键盘按键抬起，
  + `mouse move` 为鼠标滑过，`input` 输入文字。
+ 每行的第 4 个元素表示具体的动作参数
  + 当为鼠标动作时，由两个子元素构成，分别为鼠标所在的屏幕位置的横纵坐标，
  + 当为键盘动作时，由三个子元素构成，分别是（按键编号, 按键名, 拓展标记)，
  + 当为输入文字动作时，为要输入的文字内容。
+ 每行 `//` 后的部分为注释内容。
+ 修改时请严格遵守格式，否则可能导致脚本无法运行，建议修改前先备份一下。


# 使用命令行运行：

直接运行指定脚本:
```
> KeymouseGo.exe scripts/0314_1452.txt
```

运行指定脚本3次:
```
> KeymouseGo.exe scripts/0314_1452.txt 3
```


----------------------

# 赞赏支持

如果您觉得这个项目对您有所帮助，并乐意支持开源工作，可通过 `支付宝` 或 `微信支付` 为我赞赏支持

捐赠时可备注留下您的 `Github 主页地址`，我会将您加入 `感谢列表` 中（如果您愿意）

您的热情，我的动力！开源是一种精神，也是一种生活态度

<img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/donate.png" width="600">

感谢以下支持者:

<a href="https://github.com/liran319"><img src="https://avatars1.githubusercontent.com/u/4019372?s=50&v=4" height="50"></a>
<a href="https://github.com/WU731642061"><img src="https://avatars1.githubusercontent.com/u/30043630?s=50&v=4" height="50"></a>
<a href="https://github.com/FranklinDX3906"><img src="https://avatars1.githubusercontent.com/u/36653561?s=50&v=4" height="50"></a>


感谢 JetBrains 免费提供开发工具

<a href="https://www.jetbrains.com/?from=KeymouseGo"><img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/jetbrains-variant-2.png" height="80"></a>

----------------------

# 更新说明

暂时没法打包 `x86` 版本，32 位系统的同学请自行源码编译，或 [下载v1.5老版本](https://github.com/taojy123/KeymouseGo/releases/tag/v1.5) 使用


## v3.2.2

+ input 事件无法输入内容的 bug


## v3.2.1

+ 修复了中文注释无法解析的 bug


## v3.2

+ 脚本文件中可使用 `//` 进行内容注释
+ 可录制鼠标轨迹（`mouse move` 事件），并可在软件中设置轨迹精度，填 0 即不录制轨迹。


## v3.1

针对这个 issue(https://github.com/taojy123/KeymouseGo/issues/39) 增加了两个功能点

+ 命令行启动模式中可以随时按下 `F9` 热键，来终止脚本运行
+ 模拟鼠标点击的脚本语句中可以设定坐标点为 `[-1, -1]`, 用以表示在鼠标当前位置直接点击


## v3.0

因为兼容 macOS 遇到的很大的阻碍，最终放弃跨平台，血泪史可参看这两个 issue:
https://github.com/taojy123/KeymouseGo/issues/24
https://github.com/moses-palmer/pynput/issues/55

+ 改回使用 `win32api` 来模拟事件，只支持 windows 系统
+ 解决了 `shift` + `上下左右` 的回放问题，见 https://github.com/taojy123/KeymouseGo/issues/27
+ 增加了录制鼠标路径功能，需求来源 https://github.com/taojy123/KeymouseGo/issues/33
+ 增加了文字输入功能，需求来源 https://github.com/taojy123/KeymouseGo/issues/34
+ 因为使用了 `win32api`，不需要再手动设置屏幕缩放比例了
+ 录制脚本语法有部分改动，不向前兼容


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








