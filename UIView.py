# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIView.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import assets_rc

class Ui_UIView(object):
    def setupUi(self, UIView):
        if not UIView.objectName():
            UIView.setObjectName(u"UIView")
        UIView.resize(638, 463)
        icon = QIcon()
        icon.addFile(u":/pic/Mondrian.png", QSize(), QIcon.Normal, QIcon.Off)
        UIView.setWindowIcon(icon)
        self.centralwidget = QWidget(UIView)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(360, 10, 271, 191))
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_start_key = QLabel(self.groupBox)
        self.label_start_key.setObjectName(u"label_start_key")

        self.gridLayout_3.addWidget(self.label_start_key, 0, 0, 1, 1)

        self.choice_start = QComboBox(self.groupBox)
        self.choice_start.setObjectName(u"choice_start")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choice_start.sizePolicy().hasHeightForWidth())
        self.choice_start.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_start, 0, 1, 1, 1)

        self.label_record = QLabel(self.groupBox)
        self.label_record.setObjectName(u"label_record")

        self.gridLayout_3.addWidget(self.label_record, 1, 0, 1, 1)

        self.choice_record = QComboBox(self.groupBox)
        self.choice_record.setObjectName(u"choice_record")
        sizePolicy.setHeightForWidth(self.choice_record.sizePolicy().hasHeightForWidth())
        self.choice_record.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_record, 1, 1, 1, 1)

        self.label_stop = QLabel(self.groupBox)
        self.label_stop.setObjectName(u"label_stop")

        self.gridLayout_3.addWidget(self.label_stop, 2, 0, 1, 1)

        self.choice_stop = QComboBox(self.groupBox)
        self.choice_stop.setObjectName(u"choice_stop")
        sizePolicy.setHeightForWidth(self.choice_stop.sizePolicy().hasHeightForWidth())
        self.choice_stop.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_stop, 2, 1, 1, 1)

        self.label_language = QLabel(self.groupBox)
        self.label_language.setObjectName(u"label_language")

        self.gridLayout_3.addWidget(self.label_language, 3, 0, 1, 1)

        self.choice_language = QComboBox(self.groupBox)
        self.choice_language.setObjectName(u"choice_language")
        sizePolicy.setHeightForWidth(self.choice_language.sizePolicy().hasHeightForWidth())
        self.choice_language.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_language, 3, 1, 1, 1)

        self.label_extension = QLabel(self.groupBox)
        self.label_extension.setObjectName(u"label_extension")

        self.gridLayout_3.addWidget(self.label_extension, 4, 0, 1, 1)

        self.choice_extension = QComboBox(self.groupBox)
        self.choice_extension.setObjectName(u"choice_extension")
        sizePolicy.setHeightForWidth(self.choice_extension.sizePolicy().hasHeightForWidth())
        self.choice_extension.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.choice_extension, 4, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 348, 190))
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_script = QLabel(self.groupBox_2)
        self.label_script.setObjectName(u"label_script")

        self.gridLayout_2.addWidget(self.label_script, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout.setVerticalSpacing(7)
        self.gridLayout.setContentsMargins(0, 0, -1, -1)
        self.choice_script = QComboBox(self.groupBox_2)
        self.choice_script.setObjectName(u"choice_script")

        self.gridLayout.addWidget(self.choice_script, 0, 0, 1, 1)

        self.bt_open_script_files = QPushButton(self.groupBox_2)
        self.bt_open_script_files.setObjectName(u"bt_open_script_files")

        self.gridLayout.addWidget(self.bt_open_script_files, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 0, 1, 1, 1)

        self.label_run_times = QLabel(self.groupBox_2)
        self.label_run_times.setObjectName(u"label_run_times")

        self.gridLayout_2.addWidget(self.label_run_times, 1, 0, 1, 1)

        self.stimes = QSpinBox(self.groupBox_2)
        self.stimes.setObjectName(u"stimes")
        self.stimes.setMinimum(0)
        self.stimes.setMaximum(999999999)
        self.stimes.setValue(1)

        self.gridLayout_2.addWidget(self.stimes, 1, 1, 1, 1)

        self.label_mouse_interval = QLabel(self.groupBox_2)
        self.label_mouse_interval.setObjectName(u"label_mouse_interval")

        self.gridLayout_2.addWidget(self.label_mouse_interval, 2, 0, 1, 1)

        self.mouse_move_interval_ms = QSpinBox(self.groupBox_2)
        self.mouse_move_interval_ms.setObjectName(u"mouse_move_interval_ms")
        self.mouse_move_interval_ms.setMinimum(1)
        self.mouse_move_interval_ms.setMaximum(1000)
        self.mouse_move_interval_ms.setValue(100)

        self.gridLayout_2.addWidget(self.mouse_move_interval_ms, 2, 1, 1, 1)

        self.label_execute_speed = QLabel(self.groupBox_2)
        self.label_execute_speed.setObjectName(u"label_execute_speed")

        self.gridLayout_2.addWidget(self.label_execute_speed, 3, 0, 1, 1)

        self.execute_speed = QSpinBox(self.groupBox_2)
        self.execute_speed.setObjectName(u"execute_speed")
        self.execute_speed.setMinimum(20)
        self.execute_speed.setMaximum(500)
        self.execute_speed.setValue(100)

        self.gridLayout_2.addWidget(self.execute_speed, 3, 1, 1, 1)

        self.label_theme = QLabel(self.groupBox_2)
        self.label_theme.setObjectName(u"label_theme")

        self.gridLayout_2.addWidget(self.label_theme, 4, 0, 1, 1)

        self.choice_theme = QComboBox(self.groupBox_2)
        self.choice_theme.setObjectName(u"choice_theme")

        self.gridLayout_2.addWidget(self.choice_theme, 4, 1, 1, 1)

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(20, 210, 361, 41))
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
        self.verticalLayoutWidget.setGeometry(QRect(10, 260, 621, 151))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tnumrd = QLabel(self.verticalLayoutWidget)
        self.tnumrd.setObjectName(u"tnumrd")

        self.verticalLayout.addWidget(self.tnumrd)

        self.textlog = QTextEdit(self.verticalLayoutWidget)
        self.textlog.setObjectName(u"textlog")
        self.textlog.setEnabled(True)
        self.textlog.setReadOnly(True)

        self.verticalLayout.addWidget(self.textlog)

        self.formLayoutWidget_3 = QWidget(self.centralwidget)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(400, 220, 221, 31))
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

        UIView.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(UIView)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 638, 26))
        UIView.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(UIView)
        self.statusbar.setObjectName(u"statusbar")
        UIView.setStatusBar(self.statusbar)

        self.retranslateUi(UIView)

        QMetaObject.connectSlotsByName(UIView)
    # setupUi

    def retranslateUi(self, UIView):
        UIView.setWindowTitle(QCoreApplication.translate("UIView", u"KeymomuseGo v4.1", None))
        self.groupBox.setTitle(QCoreApplication.translate("UIView", u"Hotkeys", None))
        self.label_start_key.setText(QCoreApplication.translate("UIView", u"Launch/Pause", None))
        self.choice_start.setCurrentText("")
        self.label_record.setText(QCoreApplication.translate("UIView", u"Record/Pause", None))
        self.label_stop.setText(QCoreApplication.translate("UIView", u"Terminate", None))
        self.label_language.setText(QCoreApplication.translate("UIView", u"Language", None))
        self.label_extension.setText(QCoreApplication.translate("UIView", u"Extension", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("UIView", u"Config", None))
        self.label_script.setText(QCoreApplication.translate("UIView", u"Sctipt", None))
        self.bt_open_script_files.setText(QCoreApplication.translate("UIView", u"...", None))
#if QT_CONFIG(tooltip)
        self.label_run_times.setToolTip(QCoreApplication.translate("UIView", u"Execution times(0 for endless looping)", None))
#endif // QT_CONFIG(tooltip)
        self.label_run_times.setText(QCoreApplication.translate("UIView", u"Run times", None))
#if QT_CONFIG(tooltip)
        self.stimes.setToolTip(QCoreApplication.translate("UIView", u"Execution times(0 for endless looping)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_mouse_interval.setToolTip(QCoreApplication.translate("UIView", u"The smaller the value is, the preciser the trace will be", None))
#endif // QT_CONFIG(tooltip)
        self.label_mouse_interval.setText(QCoreApplication.translate("UIView", u"Mouse precision", None))
#if QT_CONFIG(tooltip)
        self.mouse_move_interval_ms.setToolTip(QCoreApplication.translate("UIView", u"The smaller the value is, the preciser the trace will be", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_execute_speed.setToolTip(QCoreApplication.translate("UIView", u"Range(20%-500%)", None))
#endif // QT_CONFIG(tooltip)
        self.label_execute_speed.setText(QCoreApplication.translate("UIView", u"Running speed(%)", None))
#if QT_CONFIG(tooltip)
        self.execute_speed.setToolTip(QCoreApplication.translate("UIView", u"Range(20%-500%)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.label_theme.setToolTip(QCoreApplication.translate("UIView", u"Range(20%-500%)", None))
#endif // QT_CONFIG(tooltip)
        self.label_theme.setText(QCoreApplication.translate("UIView", u"Theme", None))
        self.btrecord.setText(QCoreApplication.translate("UIView", u"Record", None))
        self.btrun.setText(QCoreApplication.translate("UIView", u"Launch", None))
        self.btpauserecord.setText(QCoreApplication.translate("UIView", u"Pause Record", None))
        self.tnumrd.setText(QCoreApplication.translate("UIView", u"Ready...", None))
        self.label_volume.setText(QCoreApplication.translate("UIView", u"Volume", None))
    # retranslateUi

