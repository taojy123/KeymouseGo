
from platform import system
from PySide2.QtWidgets import QLabel, QVBoxLayout, QLineEdit
from PySide2.QtCore import Signal, Qt
from PySide2.QtWidgets import QDialog


def listener_keyboard():
    if system() == 'Windows':
        win_listener_keyboard()
    elif system() in ['Linux', 'Darwin']:
        unix_listener_keyboard()
    else:
        raise OSError("Unsupported platform '{}'".format(system()))


# def get_keyboard_event(event):
#     print(event)
#     return True  


def win_listener_keyboard():
    from Recorder.WindowsRecorder import setuphook
    print('win listener keyboard')
    # print(keyboard_event)
    print('===========================')


def unix_listener_keyboard():
    pass

        
def show_dialog():
    dialog = QDialog()
    vbox_layout = QVBoxLayout()
    dialog.setLayout(vbox_layout)

    tip = QLabel('先按所需组合键, 再按enter键。')
    tip.setAlignment(Qt.AlignCenter)
    tip.setStyleSheet('font-size: 15px')
    tip.setMargin(10)

    input_hot_key = QLineEdit()
    input_hot_key.setStyleSheet('font-size: 15px')
    input_hot_key.setAlignment(Qt.AlignCenter)

    vbox_layout.addWidget(tip)
    vbox_layout.addWidget(input_hot_key)

    print('show dialog')
    listener_keyboard()

    dialog.show()
    dialog.exec_()


class Label(QLabel):

    clicked = Signal()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        show_dialog()
        # self.clear()

