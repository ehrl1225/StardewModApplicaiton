from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import FileManager
import MyWidget
from functools import partial

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.fm = FileManager

        self.open_stardew_folder = QAction(QIcon("img\\Stardew.webp"),"Opne Stardew folder")
        self.open_stardew_folder.triggered.connect(partial(self.open_folder, FileManager.openStardewFolder))
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(self.open_stardew_folder)

        self.wg = MyWidget.MyWidget(self.fm)

        self.setCentralWidget(self.wg)
        self.show()

    def open_folder(self, func):
        state = func()
        if state==-1:
            self.wg.stats_tb.append("스타듀밸리 폴더를 찾지 못했습니다.")
