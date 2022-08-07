from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from functools import partial
import FileManager
import os

class FileListItem(QWidget):
    delete_item = pyqtSignal()
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        self.lb = QLabel(self.name)
        self.btn = QPushButton("X")
        self.btn.pressed.connect(self.delete_item.emit)
        # self.btn.pressed.connect(self.pressed)
        hbox = QHBoxLayout()
        hbox.addWidget(self.lb)
        hbox.addWidget(self.btn)
        self.setLayout(hbox)

class ModFileWidget(QWidget):

    def __init__(self, fm):
        super().__init__()
        self.current_path = os.getcwd()
        self.file_list = []
        self.fm = fm
        self.initUI()

    def initUI(self):
        self.list = QListWidget()
        self.apply_btn = QPushButton("적용")

        self.list.itemDoubleClicked.connect(self.remove_file)
        self.apply_btn.pressed.connect(self.apply)
        self.setAcceptDrops(True)
        vbox = QVBoxLayout()

        vbox.addWidget(self.list)
        vbox.addWidget(self.apply_btn)

        self.setLayout(vbox)

    def apply(self):
        for i in self.file_list:
            if os.path.isdir(i):
                self.fm.apply_mod(i)
            elif os.path.isfile(i):
                _, extension = os.path.splitext(i)
                if extension == ".zip":
                    unzip_folder = self.fm.unzip_mod(i)
                    self.fm.apply_mod(unzip_folder)

    def refresh_list(self):
        self.list.clear()
        for i in self.file_list:
            self.list.addItem(i)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.file_list.append(f)
        self.refresh_list()

    def refresh_list(self):
        self.list.clear()
        for index, i in enumerate(self.file_list):
            simple_path = FileManager.simple_path(i)
            item = QListWidgetItem(self.list)
            list_item = FileListItem(simple_path)
            item.setSizeHint(list_item.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, list_item)
            list_item.delete_item.connect(partial(self.remove_file, index))

    def remove_file(self, index=None):
        if index is None:
            index = self.list.currentRow()
        if index != -1:
            self.list.takeItem(index)
            del self.file_list[index]
        self.refresh_list()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wg = ModFileWidget()
    wg.show()
    sys.exit(app.exec_())
