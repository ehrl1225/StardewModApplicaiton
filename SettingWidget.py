from PyQt5.QtWidgets import *

class SettingWidget(QWidget):

    def __init__(self, fm):
        self.fm = fm
        super().__init__()
        self.initUI()

    def initUI(self):
        self.chbs = [QCheckBox() for i in range(3)]
        self.chbs[0].setText("backup file before apply retextures")
        self.chbs[1].setText("when backup if backup folder has the file then dont")
        self.chbs[2].setText("if SMAPI is on then shutdown")

        self.apply_btn = QPushButton("apply")
        self.cancel_btn = QPushButton("cancel")

        self.apply_btn.pressed.connect(self.check)
        self.cancel_btn.pressed.connect(self.close)

        vbox = QVBoxLayout()
        for i in self.chbs:
            vbox.addWidget(i)

        hbox = QHBoxLayout()
        hbox.addWidget(self.apply_btn)
        hbox.addWidget(self.cancel_btn)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def check(self):
        self.fm.backup_file_before_apply_retextures = self.chbs[0].isChecked()
        self.fm.when_backup_if_backup_folder_has_the_file_then_dont = self.chbs[1].isChecked()
        self.fm.if_SMAPI_is_on_then_shutdown = self.chbs[2].isChecked()

    def load_settings(self):
        self.chbs[0].setCheckState(self.fm.backup_file_before_apply_retextures)
        self.chbs[1].setCheckState(self.fm.when_backup_if_backup_folder_has_the_file_then_dont)
        self.chbs[2].setCheckState(self.fm.if_SMAPI_is_on_then_shutdown)
