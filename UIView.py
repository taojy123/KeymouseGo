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
        UIView.resize(615, 290)
        icon = QIcon()
        icon.addFile(u":/pic/Mondrian.png", QSize(), QIcon.Normal, QIcon.Off)
        UIView.setWindowIcon(icon)
        self.centralwidget = QWidget(UIView)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(330, 10, 271, 161))
        self.formLayoutWidget = QWidget(self.groupBox)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 30, 251, 121))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(30)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_start_key = QLabel(self.formLayoutWidget)
        self.label_start_key.setObjectName(u"label_start_key")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_start_key)

        self.choice_start = QComboBox(self.formLayoutWidget)
        self.choice_start.setObjectName(u"choice_start")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.choice_start)

        self.label_record = QLabel(self.formLayoutWidget)
        self.label_record.setObjectName(u"label_record")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_record)

        self.choice_record = QComboBox(self.formLayoutWidget)
        self.choice_record.setObjectName(u"choice_record")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.choice_record)

        self.label_stop = QLabel(self.formLayoutWidget)
        self.label_stop.setObjectName(u"label_stop")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_stop)

        self.choice_stop = QComboBox(self.formLayoutWidget)
        self.choice_stop.setObjectName(u"choice_stop")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.choice_stop)

        self.label_language = QLabel(self.formLayoutWidget)
        self.label_language.setObjectName(u"label_language")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_language)

        self.choice_language = QComboBox(self.formLayoutWidget)
        self.choice_language.setObjectName(u"choice_language")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.choice_language)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 10, 311, 161))
        self.formLayoutWidget_2 = QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 30, 291, 121))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(20)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_script = QLabel(self.formLayoutWidget_2)
        self.label_script.setObjectName(u"label_script")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_script)

        self.choice_script = QComboBox(self.formLayoutWidget_2)
        self.choice_script.setObjectName(u"choice_script")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.choice_script)

        self.label_run_times = QLabel(self.formLayoutWidget_2)
        self.label_run_times.setObjectName(u"label_run_times")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_run_times)

        self.stimes = QSpinBox(self.formLayoutWidget_2)
        self.stimes.setObjectName(u"stimes")
        self.stimes.setMinimum(0)
        self.stimes.setMaximum(999999999)
        self.stimes.setValue(1)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.stimes)

        self.label_mouse_interval = QLabel(self.formLayoutWidget_2)
        self.label_mouse_interval.setObjectName(u"label_mouse_interval")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_mouse_interval)

        self.mouse_move_interval_ms = QSpinBox(self.formLayoutWidget_2)
        self.mouse_move_interval_ms.setObjectName(u"mouse_move_interval_ms")
        self.mouse_move_interval_ms.setMinimum(1)
        self.mouse_move_interval_ms.setMaximum(1000)
        self.mouse_move_interval_ms.setValue(100)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.mouse_move_interval_ms)

        self.label_execute_speed = QLabel(self.formLayoutWidget_2)
        self.label_execute_speed.setObjectName(u"label_execute_speed")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_execute_speed)

        self.execute_speed = QSpinBox(self.formLayoutWidget_2)
        self.execute_speed.setObjectName(u"execute_speed")
        self.execute_speed.setMinimum(20)
        self.execute_speed.setMaximum(500)
        self.execute_speed.setValue(100)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.execute_speed)

        self.tnumrd = QLabel(self.centralwidget)
        self.tnumrd.setObjectName(u"tnumrd")
        self.tnumrd.setGeometry(QRect(10, 220, 571, 20))
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(120, 180, 361, 41))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.btrecord = QPushButton(self.horizontalLayoutWidget)
        self.btrecord.setObjectName(u"btrecord")

        self.horizontalLayout.addWidget(self.btrecord)

        self.btrun = QPushButton(self.horizontalLayoutWidget)
        self.btrun.setObjectName(u"btrun")

        self.horizontalLayout.addWidget(self.btrun)

        self.btpauserecord = QPushButton(self.horizontalLayoutWidget)
        self.btpauserecord.setObjectName(u"btpauserecord")
        self.btpauserecord.setEnabled(False)

        self.horizontalLayout.addWidget(self.btpauserecord)

        UIView.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(UIView)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 615, 26))
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
        self.groupBox_2.setTitle(QCoreApplication.translate("UIView", u"Config", None))
        self.label_script.setText(QCoreApplication.translate("UIView", u"Sctipt", None))
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
        self.tnumrd.setText(QCoreApplication.translate("UIView", u"Ready...", None))
        self.btrecord.setText(QCoreApplication.translate("UIView", u"Record", None))
        self.btrun.setText(QCoreApplication.translate("UIView", u"Launch", None))
        self.btpauserecord.setText(QCoreApplication.translate("UIView", u"Pause Record", None))
    # retranslateUi

