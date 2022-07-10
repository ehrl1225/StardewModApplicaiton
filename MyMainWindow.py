from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import FileManager

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.open_steam_folder= QAction(QIcon("img\\Steam.png"),"Open Steam folder")
        self.open_stardew_folder = QAction(QIcon("img\\Stardew.webp"),"Opne Stardew folder")
        self.open_stardew_folder.triggered.connect(FileManager.openStardewFolder)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
