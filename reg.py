import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

login_ui, _ = uic.loadUiType("frontend/reg.ui")


class RegWindow(QMainWindow, login_ui):
    def __init__(self, router, db, parent=None):
        super(RegWindow, self).__init__(parent)
        self.setupUi(self)
        self.router = router
        self.db = db
        self.regButton.clicked.connect(self.reg)
        self.backButton.clicked.connect(lambda _: self.router.setCurrentIndex(0))

    def reg(self):
        login = self.loginLine.text()
        password = self.passwordLine.text()
        if len(login) > 2 and len(password) >= 8:
            self.db.add_data_to_db('users', f'"{login}", "{password}", "{datetime.datetime.now()}"')
            self.router.setCurrentIndex(2)
            self.loginLine.clear()
            self.passwordLine.clear()
        else:
            QMessageBox.critical(self, "Внимание!", "Длина пароля должа быть больше 8 символов")

