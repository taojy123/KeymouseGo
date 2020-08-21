#!/usr/bin/env python
#Boa:App:BoaApp

import os
import time
import sys
import json
import random
import traceback

from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode



def single_run(script_path, run_times=1):

    s = open(script_path, 'r').read()
    s = json.loads(s)
    steps = len(s)

    mouse_ctl = mouse.Controller()
    keyboard_ctl = keyboard.Controller()

    j = 0
    while j < run_times or run_times == 0:
        j += 1
        print('==========', j)

        # Keep the same with Frame1.py:455, and remove code include `self`
        for i in range(steps):

            print(s[i])

            # for old style script
            if isinstance(s[i][0], str) and isinstance(s[i][3], int):
                s[i].insert(0, s[i][3])

            delay = s[i][0]
            event_type = s[i][1]
            message = s[i][2]
            action = s[i][3]

            message = message.lower()
            
            time.sleep(delay / 1000.0)

            if event_type == 'EM':
                x, y = action
                mouse_ctl.position = (x, y)
                if message == 'mouse left down':
                    mouse_ctl.press(Button.left)
                elif message == 'mouse left up':
                    mouse_ctl.release(Button.left)
                elif message == 'mouse right down':
                    mouse_ctl.press(Button.right)
                elif message == 'mouse right up':
                    mouse_ctl.release(Button.right)
                else:
                    print('unknow mouse event:', message)

            elif event_type == 'EK':
                key_name = action

                if len(key_name) == 1:
                    key = key_name
                else:
                    key = getattr(Key, key_name)

                if message == 'key down':
                    keyboard_ctl.press(key)
                elif message == 'key up':
                    keyboard_ctl.release(key)
                else:
                    print('unknow keyboard event:', message)

    print('script run finish!')


try:
    fnames = os.listdir('scripts')
    if fnames:
        fname = random.choice(fnames)
        script_path = os.path.join('scripts', fname)
        print('wait 30s')
        time.sleep(30)
        print('run begin', script_path)
        single_run(script_path, 5)
except Exception as e:
    traceback.print_exc()
    input('')

print('Bye!')
