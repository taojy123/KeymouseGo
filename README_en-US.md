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
<br>

[简体中文](README.md) | [English](README_en-US.md)

</div>

Features:
  + Record mouse/keyboard operations
  + Reproduce operations recorded before
  + Can be regarded as simplified *Quick Macro*

Usage:
  + Free users away from works that are simple and repetitive
  + You can record the necessary operations once and left the rest of works to computer


# Table of content

- [KeymouseGo](#keymousego)
- [Table of content](#table-of-content)
- [Installation](#installation)
    - [Bundle with source code](#bundle-with-source-code)
- [Usage](#usage)
  - [Basic operation](#basic-operation)
    - [Desktop mode](#desktop-mode)
    - [Command line mode](#command-line-mode)
  - [Tips](#tips)
  - [Grammar of scripts](#grammar-of-scripts)
  - [Extensions](#extensions)
- [About me](#about-me)
- [Contributors](#contributors)

# Installation

This program is written in `Python` and packed as executable file. You can download [release version](https://github.com/taojy123/KeymouseGo/releases) directly without installation of Python.

### Bundle with source code

+ Windows
```
1. Install Python 3
2. pip install -r requirements-windows.txt
3. pip install pyinstaller
4. pyinstaller -F -w --add-data "./assets;assets" KeymouseGo.py
```

+ Linux or Mac
```
1. Install Python 3
2. pip3 install -r requirements-universal.txt
3. pip3 install pyinstaller
4. pyinstaller -F -w --add-data "./assets:assets" KeymouseGo.py
```

# Usage

## Basic operation

### Desktop mode

1. Click `Record` button to start recording

2. Do anything like clicking mouse or tapping keyboard, which will be recorded

3. Click `Finish` button to stop recording

4. Click `Launch` button to reproduce the operation recorded in step 2

### Command line mode

Run specific script
```
> ./KeymouseGo scripts/0314_1452.txt
```

Run specific script for 3 times
```
> ./KeymouseGo scripts/0314_1452.txt -rt 3
> ./KeymouseGo scripts/0314_1452.txt --runtimes 3
```

Run specific script at the speed of 200%
```
> ./KeymouseGo scripts/0314_1452.txt -sp 200
> ./KeymouseGo scripts/0314_1452.txt --speed 200
```

Run specific script with extension `MyExtension`
```
> ./KeymouseGo scripts/0314_1452.txt -m MyExtension
> ./KeymouseGo scripts/0314_1452.txt --module MyExtension
```

## Tips

1. The program will endlessly run the script if run times is set to `0`

2. The default launch hotkey is `F6`, which functions the same as the launch button. The default stop hotkey is `F9`, which will terminate the running script

3. Only mouse click operation and keyboard operation will be recorded. Mouse trail won't be recorded.

4. A new script file will be generated in directory `scripts` at the end of recording.

5. You can choose the script to run in choice list.

6. The content of script can be edited with reference of `Grammar of script`.

7. In hotkey setting, `Middle` refers mouse middle button and `XButton` refers mouse side button.

8. Due to the limitation of execution speed, the running speed cannot be set too high.

In some system environment, there may be circumstances that the mouse events cannot be fully recorded. To settle this, you can run this program as administrator/root.

For mac users, make sure that application must be white listed under Enable access for assistive devices. You may also need to whitelist terminal application if running from terminal. If the app crashes, you may try to give write permission for directory `~/.qt_material`.
```bash
chmod -R 770 ~/.qt_material
```

## Grammar of scripts
> Assume that the resolution of screen is `1920 * 1080`

```
[
 [3000, "EM", "mouse right down", ["0.05208%", "0.1852%"]],    // Press mouse right button at the relative coordinates `(0.05208, 0.1852)`(i.e. absolute coordinates `(100,200)`) after 3000ms
 [50,   "EM", "mouse right up",   ["0.05208%", "0.1852%"]],    // Release mouse right button at the coordinates after 50ms
 [1000, "EK", "key down",         [70, "F", 0]],                                   // Press key 'f' after 1000ms
 [50,   "EK", "key up",           [70, "F", 0]],                                   // Release key 'f' after 50ms
 [100,  "EM", "mouse left down",  ["0.2604%", "0.4630%"]],      // Press mouse left button at the relative coordinates `(0.2604, 0.4630)`(i.e. absolute coordinates `(500,500)`) after 100ms
 [100,  "EM", "mouse move",       ["0.2604%", "0.5556%"]],       // Move mouse to the relative coordinates `(0.2604, 0.4630)`(i.e. absolute coordinates `(500,500)`) after 100ms
 [100,  "EM", "mouse left up",  ["0.3125%", "0.5556%"]],                   // Release mouse left button at the relative coordinates `(0.3125, 0.5556)`(i.e. absolute coordinates `(600,600)`) after 100ms
 [100,  "EX", "input",            "Hello world"],                                   // Input 'Hello world' at current coordinate after 100ms
]
```

The script is saved in `json` format, in which each line represents a operation
+ The first element of each line is time interval(ms), indicating the interval to previous operation
+ The second element of each line is operation type. `EM` represents mouse, `EK` represents keyboard, `EX` represents extended operation
+ The third element of each line is detailed operation type, including
  + `mouse left down` :press mouse left button `mouse left up` release mouse left button
  + `mouse right down` press mouse right button`mouse right up` release mouse right button
  + `mouse middle down` press mouse middle button `mouse middle up` release mouse middle button
  + `mouse wheel up` mouse wheel slide up `mouse wheel down` mouse wheel slide down
  + `key down` press key `key up` release key
  + `mouse move` move mouse to `input` input text
+ The fourth element of each line is action type
  + If operation type is `EM`, it is consisted of coordinates of mouse.(Both relative coordinates and absolute coordinates are supported)
  + If operation type is `EK`, it is consisted of coordinates of (key number, key name, extension flag)
  + If detailed operation type is `Input`, it is the text to input
+ In each line, comment can be added after `//`
+ It is recommended to back up script before editing. And make sure to follow the format while editing, otherwise it may result in failure of execution.
+ The mouse event will execute on the position that the cursor is currently in when the coordinate is set to [-1, -1]

## Extensions

The usage of exetensions is illustrated in [wiki](https://github.com/taojy123/KeymouseGo/wiki/Document#extension)

# About me

I'm Tao Jiayuan, with commonly used id taojy123, tao.py on Internet

My personal site [tslow.cn](https://tslow.cn) organizes and lists a collection of 'personal projects' and 'gadgets'.

You can refer my newly published articles on [jianshu](http://jianshu.tslow.cn) and watch my technology sharing and life documentary on [bilibili](https://space.bilibili.com/145137942)

My Email: taojy123@163.com

----------------------

# Contributors

If you are a developer and interested in this project, you can check the progress in branch [**dev**](https://github.com/taojy123/KeymouseGo/tree/dev). and you are welcomed to participating by opening pull request to branch [**dev**](https://github.com/taojy123/KeymouseGo/tree/dev). 

Thanks to contributor:

<a href="https://github.com/Monomux"><img src="https://avatars.githubusercontent.com/u/70839036?s=80&v=4" height="80"></a> 
<a href="https://github.com/ZutJoe"><img src="https://avatars.githubusercontent.com/u/54732130?s=80&v=4" height="80"></a>


Thanks to free develop tool provided by JetBrains

<a href="https://www.jetbrains.com/?from=KeymouseGo"><img src="https://raw.githubusercontent.com/taojy123/KeymouseGo/master/jetbrains-variant-2.png" height="80"></a>

----------------------





