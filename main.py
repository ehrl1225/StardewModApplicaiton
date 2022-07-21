from PyQt5.QtWidgets import QApplication
import sys
import MyMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyMainWindow.MyMainWindow()
    sys.exit(app.exec_())