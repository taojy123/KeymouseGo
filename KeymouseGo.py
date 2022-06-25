# cython: language_level=3
# !/usr/bin/env python
# Boa:App:BoaApp
import os
import sys
import threading
import math

import pyWinhook
import pythoncom
import win32con
from PySide2.QtWidgets import QApplication, QWidget, QSpinBox
from PySide2.QtCore import QRect
from PySide2.QtGui import QFont
from PySide2 import QtCore, QtWidgets
from win32gui import GetDC
from win32print import GetDeviceCaps

import UIFunc
import argparse

from loguru import logger

from assets.plugins.ProcessException import BreakProcess, EndProcess


def add_lib_path(libpaths):
    for libpath in libpaths:
        if os.path.exists(libpath) and (libpath not in sys.path):
            sys.path.append(libpath)


add_lib_path([os.path.join(os.getcwd(), 'plugins')])


def main():

    # 适应高DPI
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ui = UIFunc.UIFunc(app)
    # 不同分辨率下调节字体大小和窗口大小
    hDC = GetDC(0)
    SW = GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    SH = GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    ratio_w = SW / 1920
    ratio_h = SH / 1080
    if ratio_w < 1:
        ratio_w = 1
    if ratio_h < 1:
        ratio_h = 1
    ui.resize(ui.width() * ratio_w, ui.height() * ratio_h)

    for q_widget in ui.findChildren(QWidget):
        # print(q_widget)
        q_widget.setGeometry(QRect(q_widget.x() * ratio_w, 
                                   q_widget.y() * ratio_h,
                                   q_widget.width() * ratio_w, 
                                   q_widget.height() * ratio_h))
        q_widget.setStyleSheet('font-size: ' + str(math.ceil(13 * min(ratio_h, ratio_w))) + 'px')
        if isinstance(q_widget, QSpinBox):
            q_widget.setStyleSheet('padding-left: 7px')

    ui.show()
    sys.exit(app.exec_())


@logger.catch
def single_run(script_path, run_times=1, speed=100, module_name='Extension'):
    t = HookThread()
    t.start()

    try:
        for path in script_path:
            logger.info('Script path:%s' % path)
            events, smodule_name = UIFunc.RunScriptClass.parsescript(path, speed=speed)
            extension = UIFunc.RunScriptClass.getextension(
                smodule_name if smodule_name is not None else module_name,
                runtimes=run_times,
                speed=speed)
            j = 0
            while j < extension.runtimes or extension.runtimes == 0:
                logger.info('===========%d==============' % j)
                try:
                    if extension.onbeforeeachloop(j):
                        UIFunc.RunScriptClass.run_script_once(events, extension)
                    extension.onaftereachloop(j)
                    j += 1
                except BreakProcess:
                    logger.debug('Break')
                    j += 1
                    continue
                except EndProcess:
                    logger.debug('End')
                    break
            extension.onendp()
            logger.info('%s run finish' % path)
        logger.info('Scripts run finish!')
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        os._exit(0)


class HookThread(threading.Thread):

    def run(self):
        def on_keyboard_event(event):
            key_name = event.Key.lower()
            stop_name = 'f9'
            if key_name == stop_name:
                logger.debug('break exit!')
                os._exit(0)
            return True

        hm = pyWinhook.HookManager()
        hm.KeyAll = on_keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()


if __name__ == '__main__':
    logger.debug(sys.argv)
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
        parser.add_argument('-m', '--module',
                            help='Extension for the program',
                            type=str,
                            default='Extension'
                            )
        args = vars(parser.parse_args())
        logger.debug(args)
        if args['speed'] <= 0:
            logger.warning('Unsupported speed')
        else:
            single_run(args['sctipts'],
                       run_times=args['runtimes'],
                       speed=args['speed'],
                       module_name=args['module']
                       )
    else:
        main()
