#!/usr/bin/env python3
""" Qt front end for scanimage program """

import sys, os
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4.QtCore import QProcess, QFile, QIODevice, QTimer, QEventLoop

sys.path.append(os.path.dirname(__file__))

from ui_mainwindow import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.comboColor.currentIndexChanged.connect(self.onColorModeChange)
        self.scanBtn.clicked.connect(self.startScanning)
        self.closeBtn.clicked.connect(self.close)
        self.format = "jpeg"
        self.filenameEdit.setText(self.newFileName())
        self.process = QProcess(self)

    def onColorModeChange(self, index):
        """ Change file format on colormode change """
        if index==2:
            self.labelExt.setText("  .tiff")
            self.format = "tiff"
        else:
            self.labelExt.setText("  .jpg")
            self.format = "jpeg"
        self.filenameEdit.setText(self.newFileName())

    def startScanning(self):
        dpi = ["100", "200", "300", "600", "1200"]
        colors = ["Color", "Gray", "Lineart"]
        page_sizes = ["None", "-x 152.4mm -y 101.6mm", "-x 215.9mm -y 279.4mm", "-x 210mm -y 297mm"]

        args = []
        args.append("--mode=" + colors[self.comboColor.currentIndex()])
        args.append("--resolution=" + dpi[self.comboResolution.currentIndex()])
        args.append("--format=" + self.format)
        if self.comboArea.currentIndex()!=0:
            args += page_sizes[self.comboArea.currentIndex()].split()
        self.statusbar.showMessage("Scan Started")
        wait(20)
        self.process.start('scanimage', args)
        if not self.process.waitForFinished() or self.process.exitCode():
            self.statusbar.showMessage("Scanning Failed !")
            return
        data = self.process.readAllStandardOutput()
        ext = ".jpg" if self.format=="jpeg" else ".tiff"
        img_file = QFile(self.filenameEdit.text() + ext, self)
        img_file.open(QIODevice.WriteOnly)
        img_file.write(data)
        data.clear()
        img_file.close()
        self.statusbar.showMessage("Scan Completed Successfully")
        self.filenameEdit.setText(self.newFileName())

    def newFileName(self):
        ext = ".jpg" if self.format=="jpeg" else ".tiff"
        index = 1
        while True:
            filename = "scan%3i" % index
            filename = filename.replace(" ", "0")
            if os.path.exists(filename + ext):
                index +=1
            else:
                break
        return filename

def wait(millisec):
    loop = QEventLoop()
    QTimer.singleShot(millisec, loop.quit)
    loop.exec_()

def main():
    app = QApplication(sys.argv)
    app.setOrganizationName("HP Scanner")
    app.setApplicationName("hp-scanner")
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
