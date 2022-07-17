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
from PySide2.QtWidgets import *
# from PySide2.QtWidgets import QApplication, QWidget, QGroupBox, QSpinBox, QPushButton, QSizePolicy
from PySide2.QtCore import QRect
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


def resize_layout(ui, ratio_w, ratio_h):
    ui.resize(ui.width() * ratio_w, ui.height() * ratio_h)

    groupboxs = []
    for q_widget in ui.findChildren(QWidget):
        if isinstance(q_widget, QPushButton):
            q_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            q_widget.setMaximumSize(250, 50)
        if not isinstance(q_widget, QGroupBox):
            q_widget.setGeometry(QRect(q_widget.x() * ratio_w, 
                                        q_widget.y() * ratio_h,
                                        q_widget.width() * ratio_w, 
                                        q_widget.height() * ratio_h))
        q_widget.setStyleSheet('font-size: ' + str(math.ceil(9 * min(ratio_h, ratio_w))) + 'px')
        if isinstance(q_widget, QSpinBox):
            q_widget.setStyleSheet('padding-left: 7px')
        if isinstance(q_widget, QGroupBox):
            groupboxs.append(q_widget)

    for groupbox in groupboxs:
        print(groupbox)
        print(f'x =======> {groupbox.x()}')
        print(f'y =======> {groupbox.y()}')
        groupbox.setGeometry(QRect(groupbox.x() * ratio_w, 
                                    groupbox.y() * ratio_h,
                                    groupbox.width() * ratio_w, 
                                    groupbox.height() * ratio_h))
        


def main():

    # 适应高DPI
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ui = UIFunc.UIFunc(app)
    # ui.findChild()
    # 不同分辨率下调节字体大小和窗口大小
    hDC = GetDC(0)
    SW = GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    SH = GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    # SW = 3840
    # SH = 2400
    ratio_w = SW / 1920
    ratio_h = SH / 1080
    print((ratio_w, ratio_h))
    # ratio_w = SW / 600
    # ratio_h = SH / 300
    if ratio_w > 1 and ratio_h > 1:
        resize_layout(ui, ratio_w, ratio_h)

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
