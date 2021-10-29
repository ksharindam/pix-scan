#!/usr/bin/env python3
""" Qt front end for scanimage program """

import sys, os
from PyQt4.QtGui import QApplication, QMainWindow, QImage, QStyle, QIcon
from PyQt4.QtCore import QProcess, QFile, QIODevice, QTimer, QEventLoop, QRect
from PyQt4 import uic

PROGRAM_DIR = os.path.dirname(__file__)
sys.path.append(PROGRAM_DIR)

ui_mainwindow, mainwindow = uic.loadUiType(PROGRAM_DIR+"/mainwindow.ui")


# get device name by `scanimage -L` . it will be like "hpaio:/usb/DeskJet_2130..."
# see scanimage options by running `scanimage --help -d "device_name"`

class HpScanner:
    def __init__(self):
        # supported values
        self.colors = ["Color", "Gray", "Lineart"]
        self.dpis = ["100", "200", "300", "600", "1200"]
        # all modes except Max Area, discards 20 pixels (2mm) from left and top
        self.page_formats =["Maximum Area", "A4 (210x297mm)",
                            "Letter (8.5x11in)", "4R (4x6in)"]
        self.scan_areas = [ "-x 215.9 -y 297.01", "-x 210 -y 297",
                            "-x 215.9 -y 279.4", "-x 152.4 -y 101.6"]
        # output formats for each color modes
        self.formats = ["jpeg", "jpeg", "tiff"]
        self.extensions = [".jpg", ".jpg", ".tiff"]
        # default values
        self.default_color_index = 0
        self.default_resolution_index = 2
        self.default_scan_area_index = 1
        self.extension = self.extensions[self.default_color_index]

    def supportedColorModes(self):
        return self.colors

    def supportedResolutions(self):
        resolutions = [x+" DPI" for x in self.dpis]
        return resolutions

    def supportedScanAreas(self):
        return self.page_formats

    def setSelectedColor(self, index):
        self.color = self.colors[index]
        self.format = self.formats[index]
        self.extension = self.extensions[index]

    def setSelectedResolution(self, index):
        self.resolution = self.dpis[index]

    def setSelectedScanArea(self, index):
        self.page_format = self.page_formats[index]
        self.scan_area = self.scan_areas[index]

    def getArgs(self):
        # get args for scanimage command
        self.crop_needed = False
        args = []
        args.append("--mode=" + self.color)
        args.append("--resolution=" + self.resolution)
        args.append("--format=" + self.format)

        # for A4 @ 300dpi , scan whole area then crop to get more accurate area
        if self.page_format.startswith("A4") and self.resolution=="300":
            self.crop_needed = True
            self.crop_rect = QRect(8,0, 2488, 3500)# theoretically 2480x3508
            return args
        if not self.page_format.startswith("Maximum"):
            args += self.scan_area.split()
        return args


class Window(mainwindow, ui_mainwindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/scanner.png"))
        scan_icon = QApplication.style().standardIcon(QStyle.SP_DialogYesButton)
        self.scanBtn.setIcon(scan_icon)
        close_icon = QApplication.style().standardIcon(QStyle.SP_DialogCloseButton)
        self.closeBtn.setIcon(close_icon)
        self.scanner = HpScanner()
        self.comboColor.addItems(self.scanner.supportedColorModes())
        self.comboResolution.addItems(self.scanner.supportedResolutions())
        self.comboArea.addItems(self.scanner.supportedScanAreas())
        # connect signals
        self.comboColor.currentIndexChanged.connect(self.onColorModeChange)
        self.scanBtn.clicked.connect(self.startScanning)
        self.closeBtn.clicked.connect(self.close)
        # Init values
        self.comboColor.setCurrentIndex(self.scanner.default_color_index)
        self.comboResolution.setCurrentIndex(self.scanner.default_resolution_index)
        self.comboArea.setCurrentIndex(self.scanner.default_scan_area_index)
        self.labelExt.setText(self.scanner.extension)
        self.filenameEdit.setText(self.newFileName())
        self.process = QProcess(self)

    def onColorModeChange(self, index):
        """ Change file format on colormode change """
        self.scanner.setSelectedColor(index)
        self.labelExt.setText(self.scanner.extension)
        self.filenameEdit.setText(self.newFileName())

    def startScanning(self):
        self.scanner.setSelectedColor(self.comboColor.currentIndex())
        self.scanner.setSelectedResolution(self.comboResolution.currentIndex())
        self.scanner.setSelectedScanArea(self.comboArea.currentIndex())
        ext = self.scanner.extension
        args = self.scanner.getArgs()

        self.statusbar.showMessage("Scan Started")
        wait(20)
        self.process.start('scanimage', args)
        if not self.process.waitForFinished() or self.process.exitCode():
            self.statusbar.showMessage("Scanning Failed !")
            return
        data = self.process.readAllStandardOutput()

        filename = self.filenameEdit.text() + ext
        # to get more accurate scanned area when A4 at 300 dpi
        if (self.scanner.crop_needed):
            image = QImage.fromData(data)
            image = image.copy(self.scanner.crop_rect)
            image.save(filename)
        else:
            img_file = QFile(filename, self)
            img_file.open(QIODevice.WriteOnly)
            img_file.write(data)
            img_file.close()
        data.clear()
        self.statusbar.showMessage("Scan Completed Successfully")
        self.filenameEdit.setText(self.newFileName())

    def newFileName(self):
        ext = self.scanner.extension
        index = 1
        while True:
            filename = "Scan%3i" % index
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
    app.setOrganizationName("pix-scan")
    app.setApplicationName("pix-scan")
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
