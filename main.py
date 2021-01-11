import sys
from PyQt5.QtWidgets import QStackedWidget, QApplication

from login import LoginWindow
from photos import PhotosWindow
from reg import RegWindow

from utils.db import DataBaseController


class Controller:
    def __init__(self):
        self.db = DataBaseController()
        self.db.create_db('users', 'name, password, date_reg')
        self.db.create_db('photos', 'id, blob, date')
        self.router = QStackedWidget()
        self.pages = [
            LoginWindow,
            RegWindow,
            PhotosWindow
        ]
        for page in self.pages:
            self.router.addWidget(page(self.router, self.db))
        self.router.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Controller()
    sys.exit(app.exec_())
