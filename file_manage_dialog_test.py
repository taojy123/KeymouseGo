from FileManageDialog import Ui_Dialog
from PySide2.QtWidgets import QApplication, QDialog

app = QApplication([])

dialog = QDialog()
Ui_Dialog().setupUi(dialog)

dialog.show()
app.exec_()