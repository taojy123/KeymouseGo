# Python3

import time
import _thread

from pynput import keyboard
from pynput.keyboard import Key, KeyCode


keyboard_ctl = keyboard.Controller()
combo_vk = None
quit = False


def combo_press(vk):
    global combo_vk
    global quit

    combo_vk = vk

    # Press `ESC` to quit
    if vk == 27:
        quit = True
        return

    print('---- start combo -----', vk)
    while vk == combo_vk:
        keyboard_ctl.press(KeyCode.from_vk(vk))
        time.sleep(0.002)
        assert vk == combo_vk
        keyboard_ctl.release(KeyCode.from_vk(vk))
        time.sleep(0.1)
    print('--------------------------')


def on_press(key):
    pass


def on_release(key):
    global combo_vk

    if isinstance(key, Key):
        print('Key:', key.name, key.value.vk)
        vk = key.value.vk
    elif isinstance(key, KeyCode):
        print('KeyCode:', key.char, key.vk)
        vk = key.vk
    else:
        assert False

    if vk == combo_vk:
        return
        
    _thread.start_new_thread(combo_press, (vk, ))


keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboard_listener.start()


print('========== MiniCombo 小连击 ===========')
print('使用时最小化该窗口，点击键盘上任意按键，开始连击')
print('如需停止或退出，请按下 ESC ')

while not quit:
    time.sleep(3)


print('bye!')
time.sleep(0.5)
