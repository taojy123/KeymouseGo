# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'file_manage.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(313, 111)
        Dialog.setWindowTitle('File Manage')
        icon = QIcon()
        icon.addFile(u":/pic/Mondrian.png", QSize(), QIcon.Normal, QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.formLayoutWidget = QWidget(Dialog)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 291, 41))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.file_name = QLabel(self.formLayoutWidget)
        self.file_name.setObjectName(u"file_name")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.file_name)

        self.lineEdit = QLineEdit(self.formLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.horizontalLayoutWidget = QWidget(Dialog)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 60, 291, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.choice = QPushButton(self.horizontalLayoutWidget)
        self.choice.setObjectName(u"choice")

        self.horizontalLayout.addWidget(self.choice)

        self.edit = QPushButton(self.horizontalLayoutWidget)
        self.edit.setObjectName(u"edit")

        self.horizontalLayout.addWidget(self.edit)

        self.rename = QPushButton(self.horizontalLayoutWidget)
        self.rename.setObjectName(u"rename")

        self.horizontalLayout.addWidget(self.rename)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.file_name.setText(QCoreApplication.translate("Dialog", u"file name", None))
        self.lineEdit.setText("")
        self.choice.setText(QCoreApplication.translate("Dialog", u"choice", None))
        self.edit.setText(QCoreApplication.translate("Dialog", u"edit", None))
        self.rename.setText(QCoreApplication.translate("Dialog", u"rename", None))
    # retranslateUi

