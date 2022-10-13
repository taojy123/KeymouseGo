# cython: language_level=3
# !/usr/bin/env python
# Boa:App:BoaApp
import os
import sys
import math

from PySide2.QtWidgets import QApplication, QWidget, QSpinBox
from PySide2.QtCore import Slot, QRect
from PySide2 import QtCore

import UIFunc
import Recorder
import argparse
from Event import ScriptEvent, ScreenWidth as SW, ScreenHeight as SH
from loguru import logger

from Util.RunScriptClass import RunScriptCMDClass, StopFlag


def to_abs_path(*args):
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                        *args)


def resize_layout(ui, ratio_w, ratio_h):
    ui.resize(ui.width() * ratio_w, ui.height() * ratio_h)

    for q_widget in ui.findChildren(QWidget):
        q_widget.setGeometry(QRect(q_widget.x() * ratio_w,
                                    q_widget.y() * ratio_h,
                                    q_widget.width() * ratio_w,
                                    q_widget.height() * ratio_h))
        q_widget.setStyleSheet('font-size: ' + str(math.ceil(9 * min(ratio_h, ratio_w))) + 'px')
        if isinstance(q_widget, QSpinBox):
            q_widget.setStyleSheet('padding-left: 7px')


def main():

    # 适应高DPI
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    ui = UIFunc.UIFunc(app)
    # 不同分辨率下调节字体大小和窗口大小
    ratio_w = SW / 1920
    ratio_h = SH / 1080
    if ratio_w > 1 and ratio_h > 1:
        resize_layout(ui, ratio_w, ratio_h)

    ui.setFixedSize(ui.width(), ui.height())
    ui.show()
    sys.exit(app.exec_())


@logger.catch
def single_run(script_path, run_times):
    flag = StopFlag(False)
    thread = RunScriptCMDClass(script_path, run_times, flag)

    stop_name = 'f9'

    @Slot(ScriptEvent)
    def on_keyboard_event(event):
        key_name = event.action[1].lower()
        if key_name == stop_name:
            logger.debug('break exit!')
            flag.flag = True
            thread.resume()
        return True

    Recorder.setuphook(commandline=True)
    Recorder.set_callback(on_keyboard_event)

    eventloop = QApplication()

    thread.finished.connect(eventloop.exit)
    thread.start()

    sys.exit(eventloop.exec_())


if __name__ == '__main__':
    logger.debug(sys.argv)
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument('scripts',
                            help='Path for the scripts',
                            type=str,
                            nargs='+'
                            )
        parser.add_argument('-rt', '--runtimes',
                            help='Run times for the script',
                            type=int,
                            default=1
                            )
        args = vars(parser.parse_args())
        logger.debug(args)
        single_run(args['scripts'],
                   run_times=args['runtimes']
                   )
    else:
        main()
