from PyQt5.QtWidgets import *
import os

class ModFileWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.current_path = os.getcwd()
        self.file_list = []
        self.initUI()

    def initUI(self):
        self.list = QListWidget()
        self.setAcceptDrops(True)
        vbox = QVBoxLayout()

        vbox.addWidget(self.list)

        self.setLayout(vbox)

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

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    wg = ModFileWidget()
    wg.show()
    sys.exit(app.exec_())