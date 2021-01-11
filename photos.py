import datetime, os
from PIL import ImageGrab
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QLabel, QDialog

main_ui, _ = uic.loadUiType("frontend/main.ui")


class ClickableLabel(QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()


class PhotosWindow(QMainWindow, main_ui):
    def __init__(self, router, db, parent=None):
        super(PhotosWindow, self).__init__(parent)
        self.setupUi(self)
        self.router = router
        self.db = db
        self.photos = []
        self.x, self.y = 0, 0

        self.db.read_blob_data()
        self.load_photos()

        self.loadButton.clicked.connect(self.save_photo)
        self.loadScreenButton.clicked.connect(self.save_screen)
        self.exitButton.clicked.connect(self.exit)

    def new_pixmap(self, file):
        self.photos.append(file)
        label = ClickableLabel()
        label.clicked.connect(label.hide)
        pixmap = QPixmap(file)
        pixmap = pixmap.scaled(256, 256, QtCore.Qt.KeepAspectRatio)
        label.setPixmap(pixmap)
        self.gridLayout.addWidget(label, self.y, self.x)
        self.x += 1
        if self.x > 2:
            self.x = 0
            self.y += 1

    def save_photo(self):
        file, _ = QFileDialog.getOpenFileName(None, 'Open File', './', "Image (*.png *.jpg *jpeg)")
        if file:
            self.db.add_blob_to_db(1, file, datetime.datetime.now())
            self.new_pixmap(file)

    def save_screen(self):
        im2 = ImageGrab.grab()
        im2.save(r"photos/screen.jpg")
        file = "photos/screen.jpg"
        self.db.add_blob_to_db(1, file, datetime.datetime.now())
        self.new_pixmap(file)

    def load_photos(self):
        try:
            for file in os.listdir('photos/'):
                file = 'photos/' + file
                self.new_pixmap(file)
            self.delete_all_photos()
        except FileNotFoundError:
            os.mkdir('photos/')
            for file in os.listdir('photos/'):
                file = 'photos/' + file
                self.new_pixmap(file)
            self.delete_all_photos()

    def delete_all_photos(self):
        for file in os.listdir('photos/'):
            os.remove('photos/' + file)

    def exit(self):
        reply = QMessageBox.question(self, 'Оповещение',
                                     "Вы точно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_all_photos()
            self.router.setCurrentIndex(0)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Оповещение',
                                     "Вы точно хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.delete_all_photos()
            event.accept()
        else:
            event.ignore()
