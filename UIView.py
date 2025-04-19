# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIView.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QSpinBox, QStatusBar, QTextEdit,
    QVBoxLayout, QWidget)
import assets_rc

class Ui_UIView(object):
    def setupUi(self, UIView):
        if not UIView.objectName():
            UIView.setObjectName(u"UIView")
        UIView.resize(651, 477)
        icon = QIcon()
        icon.addFile(u":/pic/Mondrian.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        UIView.setWindowIcon(icon)
        self.centralwidget = QWidget(UIView)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(370, 10, 271, 151))
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_language = QLabel(self.groupBox)
        self.label_language.setObjectName(u"label_language")

        self.gridLayout_3.addWidget(self.label_language, 3, 0, 1, 1)

        self.label_stop = QLabel(self.groupBox)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout_3.addWidget(self.label_stop, 2, 0, 1, 1)

        self.choice_language = QComboBox(self.groupBox)
        self.choice_language.setObjectName(u"choice_language")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choice_language.sizePolicy().hasHeightForWidth())
        self.choice_language.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_language, 3, 1, 1, 1)

        self.label_start_key = QLabel(self.groupBox)
        self.label_start_key.setObjectName(u"label_start_key")

        self.gridLayout_3.addWidget(self.label_start_key, 0, 0, 1, 1)

        self.label_record = QLabel(self.groupBox)
        self.label_record.setObjectName(u"label_record")

        self.gridLayout_3.addWidget(self.label_record, 1, 0, 1, 1)

        self.hotkey_start = QPushButton(self.groupBox)
        self.hotkey_start.setObjectName(u"hotkey_start")

        self.gridLayout_3.addWidget(self.hotkey_start, 0, 1, 1, 1)

        self.hotkey_record = QPushButton(self.groupBox)
        self.hotkey_record.setObjectName(u"hotkey_record")

        self.gridLayout_3.addWidget(self.hotkey_record, 1, 1, 1, 1)

        self.hotkey_stop = QPushButton(self.groupBox)
        self.hotkey_stop.setObjectName(u"hotkey_stop")

        self.gridLayout_3.addWidget(self.hotkey_stop, 2, 1, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 170, 361, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btrecord = QPushButton(self.horizontalLayoutWidget)
        self.btrecord.setObjectName(u"btrecord")
        sizePolicy.setHeightForWidth(self.btrecord.sizePolicy().hasHeightForWidth())
        self.btrecord.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.btrecord)

        self.btrun = QPushButton(self.horizontalLayoutWidget)
        self.btrun.setObjectName(u"btrun")
        sizePolicy.setHeightForWidth(self.btrun.sizePolicy().hasHeightForWidth())
        self.btrun.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.btrun)

        self.btpauserecord = QPushButton(self.horizontalLayoutWidget)
        self.btpauserecord.setObjectName(u"btpauserecord")
        self.btpauserecord.setEnabled(False)
        sizePolicy.setHeightForWidth(self.btpauserecord.sizePolicy().hasHeightForWidth())
        self.btpauserecord.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.btpauserecord)

        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 210, 631, 220))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tnumrd = QLabel(self.verticalLayoutWidget)
        self.tnumrd.setObjectName(u"tnumrd")

        self.horizontalLayout_2.addWidget(self.tnumrd)

        self.label_cursor_pos = QLabel(self.verticalLayoutWidget)
        self.label_cursor_pos.setObjectName(u"label_cursor_pos")
        self.label_cursor_pos.setLayoutDirection(Qt.RightToLeft)
        self.label_cursor_pos.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_cursor_pos)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.textlog = QTextEdit(self.verticalLayoutWidget)
        self.textlog.setObjectName(u"textlog")
        self.textlog.setEnabled(True)
        sizePolicy.setHeightForWidth(self.textlog.sizePolicy().hasHeightForWidth())
        self.textlog.setSizePolicy(sizePolicy)
        self.textlog.setReadOnly(True)

        self.verticalLayout.addWidget(self.textlog)

        self.formLayoutWidget_3 = QWidget(self.centralwidget)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(420, 180, 221, 31))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_volume = QLabel(self.formLayoutWidget_3)
        self.label_volume.setObjectName(u"label_volume")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_volume)

        self.volumeSlider = QSlider(self.formLayoutWidget_3)
        self.volumeSlider.setObjectName(u"volumeSlider")
        self.volumeSlider.setOrientation(Qt.Horizontal)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.volumeSlider)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 348, 151))
        self.gridLayout_4 = QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.choice_theme = QComboBox(self.groupBox_2)
        self.choice_theme.setObjectName(u"choice_theme")
        sizePolicy.setHeightForWidth(self.choice_theme.sizePolicy().hasHeightForWidth())
        self.choice_theme.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.choice_theme, 3, 1, 1, 1)

        self.label_execute_interval = QLabel(self.groupBox_2)
        self.label_execute_interval.setObjectName(u"label_execute_interval")

        self.gridLayout_4.addWidget(self.label_execute_interval, 2, 0, 1, 1)

        self.label_theme = QLabel(self.groupBox_2)
        self.label_theme.setObjectName(u"label_theme")

        self.gridLayout_4.addWidget(self.label_theme, 3, 0, 1, 1)

        self.mouse_move_interval_ms = QSpinBox(self.groupBox_2)
        self.mouse_move_interval_ms.setObjectName(u"mouse_move_interval_ms")
        sizePolicy.setHeightForWidth(self.mouse_move_interval_ms.sizePolicy().hasHeightForWidth())
        self.mouse_move_interval_ms.setSizePolicy(sizePolicy)
        self.mouse_move_interval_ms.setMinimum(1)
        self.mouse_move_interval_ms.setMaximum(1000)
        self.mouse_move_interval_ms.setValue(100)

        self.gridLayout_4.addWidget(self.mouse_move_interval_ms, 2, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.choice_script = QComboBox(self.groupBox_2)
        self.choice_script.setObjectName(u"choice_script")
        sizePolicy.setHeightForWidth(self.choice_script.sizePolicy().hasHeightForWidth())
        self.choice_script.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.choice_script, 0, 0, 1, 1)

        self.bt_open_script_files = QPushButton(self.groupBox_2)
        self.bt_open_script_files.setObjectName(u"bt_open_script_files")
        sizePolicy.setHeightForWidth(self.bt_open_script_files.sizePolicy().hasHeightForWidth())
        self.bt_open_script_files.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.bt_open_script_files, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayout_4.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.label_script = QLabel(self.groupBox_2)
        self.label_script.setObjectName(u"label_script")

        self.gridLayout_4.addWidget(self.label_script, 0, 0, 1, 1)

        self.label_run_times = QLabel(self.groupBox_2)
        self.label_run_times.setObjectName(u"label_run_times")

        self.gridLayout_4.addWidget(self.label_run_times, 1, 0, 1, 1)

        self.stimes = QSpinBox(self.groupBox_2)
        self.stimes.setObjectName(u"stimes")
        sizePolicy.setHeightForWidth(self.stimes.sizePolicy().hasHeightForWidth())
        self.stimes.setSizePolicy(sizePolicy)
        self.stimes.setMaximum(99999)
        self.stimes.setValue(1)

        self.gridLayout_4.addWidget(self.stimes, 1, 1, 1, 1)

        UIView.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(UIView)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 651, 24))
        UIView.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(UIView)
        self.statusbar.setObjectName(u"statusbar")
        UIView.setStatusBar(self.statusbar)

        self.retranslateUi(UIView)

        QMetaObject.connectSlotsByName(UIView)
    # setupUi

    def retranslateUi(self, UIView):
        UIView.setWindowTitle(QCoreApplication.translate("UIView", u"KeymouseGo v5.2.1", None))
        self.groupBox.setTitle(QCoreApplication.translate("UIView", u"Hotkeys", None))
        self.label_language.setText(QCoreApplication.translate("UIView", u"Language", None))
        self.label_stop.setText(QCoreApplication.translate("UIView", u"Terminate", None))
        self.label_start_key.setText(QCoreApplication.translate("UIView", u"Launch/Pause", None))
        self.label_record.setText(QCoreApplication.translate("UIView", u"Record/Pause", None))
        self.hotkey_start.setText("")
        self.hotkey_record.setText("")
        self.hotkey_stop.setText("")
        self.btrecord.setText(QCoreApplication.translate("UIView", u"Record", None))
        self.btrun.setText(QCoreApplication.translate("UIView", u"Launch", None))
        self.btpauserecord.setText(QCoreApplication.translate("UIView", u"Pause Record", None))
        self.tnumrd.setText(QCoreApplication.translate("UIView", u"Ready...", None))
        self.label_cursor_pos.setText(QCoreApplication.translate("UIView", u"Cursor Position:", None))
        self.label_volume.setText(QCoreApplication.translate("UIView", u"Volume", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("UIView", u"Config", None))
        self.label_execute_interval.setText(QCoreApplication.translate("UIView", u"Mouse precision", None))
        self.label_theme.setText(QCoreApplication.translate("UIView", u"Theme", None))
        self.bt_open_script_files.setText(QCoreApplication.translate("UIView", u"...", None))
        self.label_script.setText(QCoreApplication.translate("UIView", u"Script", None))
        self.label_run_times.setText(QCoreApplication.translate("UIView", u"Run times", None))
    # retranslateUi

