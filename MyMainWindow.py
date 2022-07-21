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

        self.open_steam_folder= QAction(QIcon("img\\Steam.png"),"Open Steam folder")
        self.open_stardew_folder = QAction(QIcon("img\\Stardew.webp"),"Opne Stardew folder")
        self.open_stardew_folder.triggered.connect(partial(self.open_folder, FileManager.openStardewFolder))
        self.open_steam_folder.triggered.connect(partial(self.open_folder,FileManager.openSteamFolder))
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(self.open_steam_folder)
        filemenu.addAction(self.open_stardew_folder)

        self.wg = MyWidget.MyWidget(self.fm)

        self.setCentralWidget(self.wg)
        self.show()

    def open_folder(self):
        pass
