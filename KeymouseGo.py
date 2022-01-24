#!/usr/bin/env python
#Boa:App:BoaApp

import time
import os
import sys
import json
import threading

import wx
import pyWinhook
import pythoncom

import Frame1


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

    t = HookThread()
    t.start()

    try:
        j = 0
        while j < run_times or run_times == 0:
            j += 1
            print('===========', j, '==============')
            Frame1.RunScriptClass.run_script_once(script_path, j)
        print('script run finish!')
    except Exception as e:
        raise e
    finally:
        os._exit(0)


class HookThread(threading.Thread):

    def run(self):

        def on_keyboard_event(event):
            key_name = event.Key.lower()
            stop_name = 'f9'
            if key_name == stop_name:
                print('break exit!')
                os._exit(0)
            return True

        hm = pyWinhook.HookManager()
        hm.KeyAll = on_keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()


if __name__ == '__main__':

    print(sys.argv)

    if len(sys.argv) > 1:
        script_path = sys.argv[1]
        run_times = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        single_run(script_path, run_times)
    else:
        main()

