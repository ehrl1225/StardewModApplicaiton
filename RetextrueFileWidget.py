from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from functools import partial
import FileManager
import os

class FileListItem(QWidget):
    state_changed = pyqtSignal()
    delete_item = pyqtSignal()
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        self.lb = QLabel(self.name)
        self.chb = QCheckBox()
        self.btn = QPushButton("X")
        self.chb.stateChanged.connect(self.state_changed.emit)
        self.btn.pressed.connect(self.delete_item.emit)
        hbox = QHBoxLayout()
        hbox.addWidget(self.chb)
        hbox.addWidget(self.lb)
        hbox.addWidget(self.btn)
        self.setLayout(hbox)


class RetextureFileWidget(QWidget):

    def __init__(self, fm):
        super().__init__()
        self.fm = fm
        self.current_path = FileManager.current_path
        self.file_list = []
        self.entered_folder = None
        self.checked_file={}
        self.current_items = []
        self.current_items_path = []
        self.initUI()

    def initUI(self):
        self.list = QListWidget(self)
        self.apply_character_btn = QPushButton("캐릭터 적용")
        self.apply_portrait_btn = QPushButton("초상화 적용")
        self.preview_lb = QLabel()
        self.preview_btn = QPushButton("미리보기")
        self.list.itemDoubleClicked.connect(self.enter_folder)
        self.preview_btn.pressed.connect(self.preview)
        self.apply_portrait_btn.pressed.connect(partial(self.apply_retexture,
                                                        self.fm.stardew_portrait_url,
                                                        self.fm.backup_portrait_url))
        self.apply_character_btn.pressed.connect(partial(self.apply_retexture,
                                                         self.fm.stardew_character_url,
                                                         self.fm.backup_character_url))
        self.setAcceptDrops(True)

        vbox = QVBoxLayout(self)

        hbox = QHBoxLayout()
        hbox.addWidget(self.list,2)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.preview_btn)
        vbox2.addWidget(self.preview_lb)
        hbox.addLayout(vbox2)

        vbox.addLayout(hbox)

        hbox2= QHBoxLayout()
        hbox2.addWidget(self.apply_character_btn)
        hbox2.addWidget(self.apply_portrait_btn)

        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def refresh_list(self):
        self.list.clear()
        self.current_items = []
        self.current_items_path = []
        def add_item(path, index):
            item = QListWidgetItem(self.list)
            list_item = FileListItem(path)
            item.setSizeHint(list_item.sizeHint())
            self.current_items.append(list_item)
            self.list.addItem(item)
            self.list.setItemWidget(item, list_item)
            list_item.delete_item.connect(partial(self.remove_file, index))
            list_item.state_changed.connect(partial(self.checked, index))
            return list_item

        if self.entered_folder is None:
            for index, i in enumerate(self.file_list):
                simple_path = FileManager.simple_path(i)
                self.current_items_path.append(simple_path)
                item = add_item(simple_path, index)
                item.chb.setCheckState(self.checked_file[i]["checked"])
        else:
            simple_path = FileManager.simple_path(self.entered_folder)
            self.list.addItem(f"{simple_path} (돌아가기)")

            for index, i in enumerate(os.listdir(self.entered_folder)):
                real_path = os.path.join(self.entered_folder,i)
                self.current_items_path.append(real_path)
                item = add_item(i,index)
                item.chb.setCheckState(self.checked_file[self.entered_folder]["files"][real_path]["checked"])

    def checked(self, index):
        path = self.current_items_path[index]
        state = self.current_items[index].chb.checkState()
        if self.entered_folder:
            self.checked_file[self.entered_folder]["files"][path]["checked"]=state
            for i in self.checked_file[self.entered_folder]["files"].keys():
                if self.checked_file[self.entered_folder]["files"][i]["checked"] == 0:
                    self.checked_file[self.entered_folder]["checked"]=0
                    break
            else:
                self.checked_file[self.entered_folder]["checked"] = 2

        elif self.entered_folder is None:
            self.checked_file[path]["checked"] = state
            if os.path.isdir(path):
                for i in self.checked_file[path]["files"].keys():
                    self.checked_file[path]["files"][i]["checked"] = state

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            self.file_list.append(f)
            if os.path.isdir(f):
                self.checked_file[f] = {
                    "files" : {},
                    "checked" : 0
                }
                for i in os.listdir(f):
                    self.checked_file[f]["files"][os.path.join(f,i)]={"checked":0}
            else:
                self.checked_file[f]={"checked":0}
        self.refresh_list()
        self.preview()

    def remove_file(self, index=None):
        if index is None:
            index = self.list.currentRow()
        if index != -1:
            self.list.takeItem(index)
            if self.entered_folder is None:
                del self.file_list[index]
        self.refresh_list()
        self.preview()

    def preview(self):
        current_index = self.list.currentRow()

        if current_index!=-1:
            if self.entered_folder:
                pixmap = FileManager.xnb_to_img(self.current_items_path[current_index-1])
            else:
                pixmap = FileManager.xnb_to_img(self.current_items_path[current_index])
            self.preview_lb.setPixmap(pixmap)
        else:
            pixmap = QPixmap("img\\Stardew.webp")
            self.preview_lb.setPixmap(pixmap)

    def enter_folder(self):
        index = self.list.currentRow()
        file_path = self.file_list[index]
        if self.entered_folder is not None and index==0:
            self.entered_folder = None
            self.refresh_list()
        elif os.path.isdir(file_path):
            self.entered_folder = file_path
            self.refresh_list()

    def selected_files(self):
        files = []
        for i in self.checked_file.keys():
            if self.checked_file[i]["checked"]==2:
                if os.path.isfile(i):
                    files.append(i)
                elif os.path.isdir(i):
                    for j in self.checked_file[i]["files"].keys():
                        files.append(j)
            elif self.checked_file[i]["checked"]==0:
                if os.path.isdir(i):
                    for j in self.checked_file[i]["files"].keys():
                        if self.checked_file[i]["files"][j]["checked"]==2:
                            files.append(j)
        return files

    def apply_retexture(self, apply_to_folder, backup_folder):
        for i in self.selected_files():
            self.fm.apply_retexture(i,apply_to_folder, backup_folder)

if __name__ == '__main__':
    import sys
    fm = FileManager
    app = QApplication(sys.argv)
    wg = RetextureFileWidget(fm)
    wg.show()
    sys.exit(app.exec_())
