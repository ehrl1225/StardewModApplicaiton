from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import FileManager
import MyWidget
import SettingWidget
import Worker
from functools import partial

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.fm = FileManager
        self.fm.load_cash()
        self.worker = Worker.Worker()
        self.setting_wg = SettingWidget.SettingWidget(self.fm)
        self.wg = MyWidget.MyWidget(self.fm)

        self.show_setting_wg = QAction("Show setting widget")
        self.show_setting_wg.triggered.connect(self.setting_wg.show)
        self.open_stardew_folder = QAction(QIcon("img\\Stardew.webp"),"Opne Stardew folder")
        self.open_stardew_folder.triggered.connect(partial(self.open_folder, FileManager.openStardewFolder))

        self.worker.start()

        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(self.open_stardew_folder)
        filemenu.addAction(self.show_setting_wg)


        self.setCentralWidget(self.wg)
        self.show()

    @pyqtSlot(str)
    def add_log(self, log):
        self.wg.add_log(log)

    @pyqtSlot(list)
    def add_job(self, job):
        for i in job:
            self.worker.jobs.append(i)

    def open_folder(self, func):
        state = func()
        if state==-1:
            self.wg.stats_tb.append("스타듀밸리 폴더를 찾지 못했습니다.")

    def closeEvent(self, e):
        self.fm.save_cash()
        self.worker.stop()
        e.accept()
