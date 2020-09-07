#!/usr/bin/env python
#Boa:App:BoaApp

import os
import time
import sys
import json
import random
import traceback
import tkinter
import _thread

import win32con
import win32api
import ctypes



def single_run(script_path, run_times=1):

    s = open(script_path, 'r').read()
    s = json.loads(s)
    steps = len(s)

    j = 0
    while j < run_times or run_times == 0:
        j += 1
        print('==========', j)

        # Keep the same with Frame1.py:455, and remove code include `self`
        for i in range(steps):

            print(s[i])
            # [782, "EM", "mouse left down", [1050, 434]]

            # for old style script
            if isinstance(s[i][0], str) and isinstance(s[i][3], int):
                # ["EM", "mouse left down", [1050, 434], 782] => [782, "EM", "mouse left down", [1050, 434], 782]
                s[i].insert(0, s[i][3])

            delay = s[i][0]
            event_type = s[i][1]
            message = s[i][2]
            action = s[i][3]

            message = message.lower()
            
            time.sleep(delay / 1000.0)

            if event_type == 'EM':
                x, y = action

                ctypes.windll.user32.SetCursorPos(x, y)

                if message == 'mouse left down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                elif message == 'mouse left up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif message == 'mouse right down':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                elif message == 'mouse right up':
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                else:
                    print('unknow mouse event:', message)

            elif event_type == 'EK':
                key_code, key_name = action

                if key_code >= 160 and key_code <= 165:
                    key_code = int(key_code / 2) - 64

                if message == 'key down':
                    win32api.keybd_event(key_code, 0, 0, 0)  
                elif message == 'key up':
                    win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)
                else:
                    print('unknow keyboard event:', message)

    print('script run finish!')


def run():
    try:
        fnames = list(os.listdir('scripts'))
        print(fnames)
        if fnames:
            n = int(time.time()) % len(fnames)
            fname = fnames[n]
            print('choice file:', fname)
            script_path = os.path.join('scripts', fname)
            print('wait 30s')
            time.sleep(30)
            print('run begin', script_path)
            single_run(script_path, 5)
            print('exit..')
            top.quit()
    except Exception as e:
        exc = traceback.format_exc()
        print(exc)


def print_to_tk(*args):
    args = [str(arg) for arg in args]
    text = ' '.join(args)
    # t1.delete('0.0', 'end')
    t1.insert('end', text + '\n')

print = print_to_tk
top = tkinter.Tk()
top.geometry('+0+0')
t1 = tkinter.Text(top, width=30, height=15)
t1.pack()
top.state('iconic')

_thread.start_new_thread(run, ())

top.mainloop()

