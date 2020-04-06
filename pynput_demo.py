# pip intall pynput


from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode
import time


# ============ mouse hook ============ 
def on_move(x, y):
    pass

def on_scroll(x, y, dx, dy):
    pass

def on_click(x, y, button, pressed):
    print('---- mouse hook -----')
    print(x, y, button.name, pressed)
    print('---------------------')

mouse_listener = mouse.Listener(
    on_move=on_move,
    on_scroll=on_scroll,
    on_click=on_click
)
mouse_listener.start()

time.sleep(1)


# ============ mouse control ============ 
mouse_ctl = mouse.Controller()
mouse_ctl.position = (100, 200)
mouse_ctl.press(Button.left)
mouse_ctl.position = (100, 150)
mouse_ctl.release(Button.left)
# mouse_ctl.scroll(0, 2)


time.sleep(1)


# ============ keyboard hook ============ 
def on_press(key):
    print('---- keyboard hook -----')
    if isinstance(key, Key):
        print('Key:', key.name, key.value.vk)
    elif isinstance(key, KeyCode):
        print('KeyCode:', key.char, key.vk)
    else:
        assert False
    print('------------------------')


def on_release(key):
    pass

keyboard_listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
keyboard_listener.start()


time.sleep(1)


# ============ keyboard control ============ 
keyboard_ctl = keyboard.Controller()

keyboard_ctl.press('a')
keyboard_ctl.release('a')

keyboard_ctl.press(KeyCode.from_char('b'))
keyboard_ctl.release(KeyCode.from_char('b'))

keyboard_ctl.press(Key.space)
keyboard_ctl.release(Key.space)

keyboard_ctl.press(getattr(Key, 'shift'))
keyboard_ctl.press('c')
keyboard_ctl.release('c')
keyboard_ctl.release(getattr(Key, 'shift'))

keyboard_ctl.press(KeyCode.from_vk(11))
keyboard_ctl.release(KeyCode.from_vk(11))

time.sleep(5)

