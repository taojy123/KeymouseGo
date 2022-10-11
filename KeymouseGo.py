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
from Util.Parser import LegacyParser
from Util.RunScriptClass import RunScriptClass


def add_lib_path(libpaths):
    for libpath in libpaths:
        if os.path.exists(libpath) and (libpath not in sys.path):
            sys.path.append(libpath)


def to_abs_path(*args):
    return os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),
                        *args)


add_lib_path([os.path.join(to_abs_path('plugins'))])


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

    ui.show()
    sys.exit(app.exec_())


@logger.catch
def single_run(script_path, run_times=1):
    @Slot(ScriptEvent)
    def on_keyboard_event(event):
        key_name = event.action[1].lower()
        stop_name = 'f9'
        if key_name == stop_name:
            logger.debug('break exit!')
            os._exit(0)
        return True

    Recorder.setuphook(commandline=True)
    Recorder.set_callback(on_keyboard_event)

    try:
        for path in script_path:
            logger.info('Script path:%s' % path)
            events = LegacyParser.parse(path)
            j = 0
            while j < run_times or run_times == 0:
                logger.info('===========%d==============' % j)
                RunScriptClass.run_script_once(events)
                j += 1
            logger.info('%s run finish' % path)
        logger.info('Scripts run finish!')
    except Exception as e:
        logger.error(e)
        raise e
    finally:
        os._exit(0)


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
