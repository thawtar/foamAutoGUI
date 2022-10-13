import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.process = QProcess(self)
        self.terminal = QWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.terminal)
        wid = str(int(self.terminal.winId()))
        self.process.start('urxvt', ['-embed', wid])

    def closeEvent(self, event):
        self.process.terminate()
        self.process.waitForFinished(1000)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
