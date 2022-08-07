from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    done = pyqtSignal()
    add_log = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.jobs = []
        self.power = True

    def run(self):
        while True:
            if not self.power:
                break
            elif not self.jobs:
                self.wait(100)
                continue
            else:
                log = self.jobs[0]()
                self.add_log.emit(log)
                del self.jobs

    def stop(self):
        self.power = False
        self.quit()
        self.wait(3000)
