#!/usr/bin/env python
#Boa:App:BoaApp

import Frame1
import wx
import time
import sys
import json

from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key, KeyCode


modules = {'Frame1': [1, 'Main frame of Application', u'Frame1.py']}


class BoaApp(wx.App):
    def OnInit(self):
        self.main = Frame1.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    application = BoaApp(0)
    application.MainLoop()


def single_run(script_path, run_times=1):

    # python KeymouseGo.py scripts/0416_2342.txt 10
    # KeymouseGo.exe scripts\0416_2342.txt

    s = open(script_path, 'r').read()
    s = json.loads(s)
    steps = len(s)

    mouse_ctl = mouse.Controller()
    keyboard_ctl = keyboard.Controller()

    j = 0
    while j < run_times or run_times == 0:
        j += 1

        for i in range(0, steps):

            print(s[i])

            event_type = s[i][0]
            message = s[i][1]
            delay = s[i][3]

            time.sleep(delay / 1000.0)

            if event_type == 'EM':
                x, y = s[i][2]
                mouse_ctl.position = (x, y)
                if message == 'mouse left down':
                    mouse_ctl.press(Button.left)
                elif message == 'mouse left up':
                    mouse_ctl.release(Button.left)
                elif message == 'mouse right down':
                    mouse_ctl.press(Button.right)
                elif message == 'mouse right up':
                    mouse_ctl.release(Button.right)

            elif event_type == 'EK':
                key_name = s[i][2]

                if len(key_name) == 1:
                    key = key_name
                else:
                    key = getattr(Key, key_name)

                if message == 'key down':
                    keyboard_ctl.press(key)
                elif message == 'key up':
                    keyboard_ctl.release(key)

    print('script run finish!')


if __name__ == '__main__':

    print(sys.argv)

    if len(sys.argv) > 1:
        script_path = sys.argv[1]
        run_times = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        single_run(script_path, run_times)
    else:
        main()

