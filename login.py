from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox

login_ui, _ = uic.loadUiType("frontend/login.ui")


class LoginWindow(QMainWindow, login_ui):
    def __init__(self, router, db, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.router = router
        self.db = db
        self.loginButton.clicked.connect(self.auth)
        self.regButton.clicked.connect(lambda _: self.router.setCurrentIndex(1))

    def auth(self):
        if self.db.get_user_with_filter(f'name="{self.loginLine.text()}" AND password="{self.passwordLine.text()}"') \
                is not None:
            self.router.setCurrentIndex(2)
            self.loginLine.clear()
            self.passwordLine.clear()
        else:
            QMessageBox.critical(self, "Внимание!", "Ошибка в логине или пароле!")
