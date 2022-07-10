from PyQt5.QtWidgets import *
import ModFileWidget

class MyWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.file_path_le = QLineEdit()
        self.file_search_btn = QPushButton("...")

        self.mod_file_wg = ModFileWidget.ModFileWidget()
        self.moded_file_list = QListWidget()

        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.file_path_le)
        hbox1.addWidget(self.file_search_btn)

        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.mod_file_wg)
        hbox2.addWidget(self.moded_file_list)

        vbox.addLayout(hbox2)

        self.setLayout(vbox)

    def loadSteamFolder(self):
        folder_name = QFileDialog()
        name = folder_name.getExistingDirectory()
        self.file_path_le.setText(name)
