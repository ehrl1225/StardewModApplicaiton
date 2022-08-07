import os.path

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
import FileManager


class StardewModsWidget(QWidget):
    add_log = pyqtSignal(str)
    def __init__(self, fm):
        super().__init__()
        self.fm = fm
        self.list_items = []
        self.initUI()

    def initUI(self):
        self.refresh_btn = QPushButton("새로고침")
        self.list = QListWidget()
        self.remove_btn = QPushButton("제거")

        self.refresh_btn.pressed.connect(self.refresh)
        self.remove_btn.pressed.connect(self.remove)

        vbox = QVBoxLayout()
        vbox.addWidget(self.refresh_btn)
        vbox.addWidget(self.list)
        vbox.addWidget(self.refresh_btn)

        self.setLayout(vbox)

    def refresh(self):
        self.list_items = []
        self.list.clear()
        if os.path.isdir(FileManager.stardew_mods_url):
            for i in self.fm.loadMods():
                item = QListWidgetItem(self.list)
                list_item = QCheckBox(i)
                item.setSizeHint(list_item.sizeHint())
                self.list.addItem(item)
                self.list.setItemWidget(item, list_item)
                self.list_items.append(list_item)

    def remove(self):
        for index, i in enumerate(self.list_items[::-1]):
            if i.checkState()==2:
                state = FileManager.remove_stardew_mod(i)
                if state:
                    self.list.takeItem(len(self.list_items)-1*(i+1))
                    self.add_log.emit(f"모드 {i.text()} 삭제됨")
                else:
                    self.add_log.emit("모드 삭제가 거부되었습니다.")
