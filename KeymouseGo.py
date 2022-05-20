# cython: language_level=3
# !/usr/bin/env python
# Boa:App:BoaApp
import os
import sys
import threading

import pyWinhook
import pythoncom
from PySide2 import QtWidgets

import UIFunc
import argparse

from qt_material import apply_stylesheet
# DPI感知
# try:
#     # win10 version 1607及以上
#     ctypes.windll.shcore.SetProcessDpiAwarenessContext(ctypes.windll.shcore.DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
# except:
#     try:
#         # win 8.1 及以上
#         ctypes.windll.shcore.SetProcessDpiAwareness(ctypes.windll.shcore.PROCESS_PER_MONITOR_DPI_AWARE)
#     except:
#         # win vista 及以上
#         ctypes.windll.user32.SetProcessDPIAware()
#


def main():
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='light_cyan_500.xml')
    ui = UIFunc.UIFunc()
    ui.show()
    sys.exit(app.exec_())


def single_run(script_path, run_times=1, speed=100):
    t = HookThread()
    t.start()

    try:
        for path in script_path:
            print(path)
            events = UIFunc.RunScriptClass.parsescript(path, speed=speed)
            j = 0
            while j < run_times or run_times == 0:
                j += 1
                print('===========', j, '==============')
                UIFunc.RunScriptClass.run_script_once(events, j)
            print(path + 'run finish')
        print('scripts run finish!')
    except Exception as e:
        print(e)
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
        parser = argparse.ArgumentParser()
        parser.add_argument('sctipts',
                            help='Path for the scripts',
                            type=str,
                            nargs='+'
                            )
        parser.add_argument('-rt', '--runtimes',
                            help='Run times for the script',
                            type=int,
                            default=1
                            )
        parser.add_argument('-sp', '--speed',
                            help='Run speed for the script, input in percentage form',
                            type=int,
                            default=100
                            )
        args = vars(parser.parse_args())
        print(args)
        if args['speed'] <= 0:
            print('Unsupported speed')
        else:
            single_run(args['sctipts'],
                       run_times=args['runtimes'],
                       speed=args['speed']
                       )
    else:
        main()
