import os.path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
import ModFileWidget
import RetextrueFileWidget
import StardewModsWidget
import FileManager

class MyWidget(QWidget):

    def __init__(self, fm):
        super().__init__()
        self.fm = fm
        self.initUI()

    def initUI(self):
        self.lbs = [QLabel() for _ in range(1)]

        self.lbs[0].setText("스타듀밸리 폴더")

        self.file_path_le = QLineEdit()
        self.file_search_btn = QPushButton("...")

        self.file_tabs = QTabWidget()

        self.mod_file_wg = ModFileWidget.ModFileWidget(self.fm)
        self.retext_file_wg = RetextrueFileWidget.RetextureFileWidget(self.fm)
        self.stardew_mods_wg = StardewModsWidget.StardewModsWidget(self.fm)
        self.stats_tb = QTextBrowser()

        self.file_path_le.setText(self.fm.stardew_url)

        self.file_tabs.addTab(self.mod_file_wg,"적용할 모드")
        self.file_tabs.addTab(self.retext_file_wg, "적용할 리텍")
        self.file_tabs.addTab(self.stardew_mods_wg,"적용된 모드")
        self.file_tabs.tabBarClicked.connect(self.tab_changed)


        self.file_search_btn.pressed.connect(self.show_file_dialog)

        vbox = QVBoxLayout()

        vbox.addWidget(self.lbs[0])

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.file_path_le)
        hbox1.addWidget(self.file_search_btn)

        vbox.addLayout(hbox1)

        vbox.addWidget(self.file_tabs)
        vbox.addWidget(self.stats_tb)

        self.setLayout(vbox)

    def loadSteamFolder(self):
        folder_name = QFileDialog()
        name = folder_name.getExistingDirectory()
        self.file_path_le.setText(name)

    def set_stardew_folder(self):
        self.fm.stardew_url = self.file_path_le.text()
        self.fm.stardew_mods_url = os.path.join(self.fm.stardew_url, "Mods")
        self.fm.stardew_portrait_url = os.path.join(self.fm.stardew_url, "Content", "Portraits")
        self.fm.stardew_character_url = os.path.join(self.fm.stardew_url, "Content", "Characters")

    def show_file_dialog(self):
        dir_name = QFileDialog.getExistingDirectory()
        if dir_name:
            self.file_path_le.setText(dir_name)
            self.set_stardew_folder()

    def tab_changed(self):
        index = self.file_tabs.currentIndex()
        if index ==2:
            self.stardew_mods_wg.refresh()

    @pyqtSlot(str)
    def add_log(self, text):
        self.stats_tb.append(text)
