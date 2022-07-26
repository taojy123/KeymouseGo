import os
import re
import platform
import subprocess
from PySide2.QtWidgets import QDialog, QFileDialog, QInputDialog
from PySide2.QtWidgets import QMainWindow, QMessageBox

from UIFileManageDialogView import Ui_Dialog
from UIFunc import scripts, scripts_map


class FileDialog(Ui_Dialog):
    def __init__(self):
        self.dialog = QDialog()
        self.setupUi(self.dialog)
        self.choice.clicked.connect(self.choice_file)
        self.edit.clicked.connect(self.edit_file)
        self.rename.clicked.connect(self.rename_file)

        self.main_window = QMainWindow()
        self.filename = scripts[scripts_map['current_index']]
        self.lineEdit.setText(self.filename)
        self.path = os.path.join(os.getcwd(), "scripts")
        i18n_language = {
            '简体中文': ['文件管理', '当前文件', '选择文件', '编辑脚本', '重命名', '文件没有被找到', '请输入新文件名: ', '更新成功', '文件名不能为空或空格'], 
            'English': ['File Manage', 'Current file', 'Choice', 'Edit', 'Rename', 'File not found', 'Please input new name', 'Success', 'File name cannot be empty or space']
            }
        self.language = i18n_language[scripts_map['choice_language']]
        
        self.dialog.setWindowTitle(self.language[0])
        self.file_name.setText(self.language[1])
        self.choice.setText(self.language[2])
        self.edit.setText(self.language[3])
        self.rename.setText(self.language[4])
    

    def choice_file(self):
        file = QFileDialog.getOpenFileName(self.main_window, "选择文件", dir='scripts', filter='*.txt')[0]
        file_name = re.split(r'\\|\/', file)[-1]
        if file_name.strip() != '' and file_name is not None:
            self.lineEdit.setText(file_name)


    def edit_file(self):
        # Mac打开文件防止以后需要
        # if userPlatform == 'Darwin':
        #     subprocess.call(['open', filename.get()])
        user_paltform = platform.system()
        try:
            if user_paltform == 'Linux':
                subprocess.call(['xdg-open', os.path.join(self.path, self.lineEdit.text())])
            else:
                os.startfile(os.path.join(self.path, self.lineEdit.text()))
        except FileNotFoundError:
            QMessageBox().warning(self.main_window, "warning", self.language[5])
            self.lineEdit.setText('')


    def rename_file(self):
        new_file_name = str(QInputDialog.getText(self.main_window, self.language[4], self.language[6])[0])

        if new_file_name != None and new_file_name.strip() != '':
            if not new_file_name.endswith('.txt'):
                new_file_name = new_file_name + '.txt'

            try:
                os.rename(os.path.join(self.path, self.lineEdit.text()), os.path.join(self.path, new_file_name))
                QMessageBox().information(self.main_window, 'info', self.language[7])
                # 更新
                filename = self.lineEdit.text()
                index = scripts_map.get(filename)
                scripts_map.pop(filename)
                scripts_map[new_file_name] = index
                scripts[index] = new_file_name
                self.lineEdit.setText(new_file_name)
            except FileNotFoundError:
                QMessageBox.warning(self.main_window, 'warning', self.language[5])
        else:
            QMessageBox.warning(self.main_window, 'warning', self.language[8])


    def show(self):
        self.dialog.show()
        self.dialog.exec_()
        
