#!/usr/bin/env python3
""" Qt front end for scanimage program """

import sys, os
from PyQt5.QtGui import QImage, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStyle
from PyQt5.QtCore import QProcess, QFile, QIODevice, QTimer, QEventLoop, QRect
from PyQt5 import uic

PROGRAM_DIR = os.path.dirname(__file__)
sys.path.append(PROGRAM_DIR)

ui_mainwindow, mainwindow = uic.loadUiType(PROGRAM_DIR+"/mainwindow.ui")


# get device name by `scanimage -L` . it will be like "hpaio:/usb/DeskJet_2130..."
# device `brother5:bus2;dev3' is a Brother DCP-T420W USB scanner

# see scanimage options by running `scanimage --help -d "device_name"`

# view formatted device name
# scanimage -f "%v %m%n"


class DummyScanner:
    def __init__(self, device):
        self.device = device
        # supported values
        self.colors = ["Color"]
        self.dpis = ["200"]
        # all modes except Max Area, discards 20 pixels (2mm) from left and top
        self.page_formats =["Maximum Area"]
        # Brother T420W uses rounded value in steps of 0.0999908
        # thus 215.9 becomes 215.88 and 297 becomes 296.973
        self.scan_areas = [ "-x 215.88 -y 296.973"]
        # output formats for each color modes
        self.formats = ["jpeg"]
        self.extensions = [".jpg"]
        # default values
        self.default_color_index = 0
        self.default_resolution_index = 0
        self.default_scan_area_index = 0
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
        args = ["-d", self.device]
        return args


class HpScanner:
    def __init__(self, device):
        self.device = device
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
        args = ["-d", self.device]
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



class EpsonScanner:
    def __init__(self, device):
        self.device = device
        # supported values
        self.colors = ["Color", "Grayscale", "Monochrome"]
        self.dpis = ["100", "200", "300", "600", "1200"]
        # all modes except Max Area, discards 20 pixels (2mm) from left and top
        self.page_formats =["Maximum Area", "A4 (210x297mm)",
                            "Letter (8.5x11in)", "4R (4x6in)"]
        self.scan_areas = [ "-x 215.9 -y 297.18", "-x 210 -y 297",
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
        args = ["-d", self.device]
        args.append("--mode=" + self.color)
        args.append("--resolution=" + self.resolution)
        args.append("--format=" + self.format)
        args.append("--brightness=20")
        #args.append("--contrast=10")

        if not self.page_format.startswith("Maximum"):
            args += self.scan_area.split()
        return args



class BrotherScanner:
    def __init__(self, device):
        self.device = device
        # supported values
        self.colors = ["24bit Color", "True Gray", "Black & White", "Gray[Error Diffusion]"]
        self.dpis = ["100", "200", "300", "400", "600"]
        # all modes except Max Area, discards 20 pixels (2mm) from left and top
        self.page_formats =["Maximum Area", "A4 (210x297mm)",
                            "Letter (8.5x11in)", "4R (4x6in)"]
        # Brother T420W uses rounded value in steps of 0.0999908
        # thus 215.9 becomes 215.88 and 297 becomes 296.973
        self.scan_areas = [ "-x 215.88 -y 296.973", "-x 210 -y 296.973",
                            "-x 215.9 -y 279.4", "-x 152.4 -y 101.6"]
        # output formats for each color modes
        self.formats = ["jpeg", "jpeg", "tiff", "tiff"]
        self.extensions = [".jpg", ".jpg", ".tiff", ".tiff"]
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
        args = ["-d", self.device]
        args.append("--mode=" + self.color)
        args.append("--resolution=" + self.resolution)
        args.append("--format=" + self.format)

        if not self.page_format.startswith("Maximum"):
            args += self.scan_area.split()
        return args



class CanonScanner:
    def __init__(self, device):
        self.device = device
        # supported values
        self.colors = ["Color", "Gray", "Lineart"]
        self.dpis = ["75", "150", "300", "600"]
        # all modes except Max Area, discards 20 pixels (2mm) from left and top
        self.page_formats =["Maximum Area", "A4", "Letter", "4R"]
        # Brother T420W uses rounded value in steps of 0.0999908
        # thus 215.9 becomes 215.88 and 297 becomes 296.973
        self.scan_areas = [ "-x 216.069 -y 297.011", "-x 210 -y 297.011",
                            "-x 216.069 -y 279.4", "-x 152.4 -y 101.6"]
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
        args = ["-d", self.device]
        args.append("--mode=" + self.color)
        args.append("--resolution=" + self.resolution)
        args.append("--format=" + self.format)

        if not self.page_format.startswith("Maximum"):
            args += self.scan_area.split()
        return args



class Window(mainwindow, ui_mainwindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(":/scanner.png"))
        QIcon.setThemeName("Adwaita")
        self.setupUi(self)
        close_icon = QApplication.style().standardIcon(QStyle.SP_DialogCloseButton)
        self.closeBtn.setIcon(close_icon)

        # connect signals
        self.comboDevice.currentIndexChanged.connect(self.onDeviceChange)
        self.comboColor.currentIndexChanged.connect(self.onColorModeChange)
        self.scanBtn.clicked.connect(self.startScanning)
        self.closeBtn.clicked.connect(self.close)

        self.process = QProcess(self)
        QTimer.singleShot(100, self.updateDeviceList)

    def updateDeviceList(self):
        self.devices_info = get_devices()
        if len(self.devices_info)>0:
            self.comboDevice.clear()
            models = [ dev['model'] for dev in self.devices_info]
            self.comboDevice.addItems(models)
            vendors = [ dev['vendor'] for dev in self.devices_info]
            # Sorted according to scan quality
            for vendor in ['HEWLETT-PACKARD', 'CANON', 'EPSON', 'BROTHER']:
                if vendor in vendors:
                    i = vendors.index(vendor)
                    self.comboDevice.setCurrentIndex(i)
                    break


    def selectDevice(self, index):
        self.scanner = get_backend_from_scanner_device(self.devices_info[index])

        self.comboColor.clear()
        self.comboResolution.clear()
        self.comboArea.clear()
        self.comboColor.addItems(self.scanner.supportedColorModes())
        self.comboResolution.addItems(self.scanner.supportedResolutions())
        self.comboArea.addItems(self.scanner.supportedScanAreas())

        # Init values
        self.comboColor.setCurrentIndex(self.scanner.default_color_index)
        self.comboResolution.setCurrentIndex(self.scanner.default_resolution_index)
        self.comboArea.setCurrentIndex(self.scanner.default_scan_area_index)
        self.labelExt.setText(self.scanner.extension)
        self.filenameEdit.setText(self.newFileName())

    def onDeviceChange(self, index):
        self.selectDevice(index)

    def onColorModeChange(self, index):
        """ Change file format on colormode change """
        self.scanner.setSelectedColor(index)
        self.labelExt.setText(self.scanner.extension)
        self.filenameEdit.setText(self.newFileName())

    def startScanning(self):
        if self.comboDevice.count()==0:
            return
        self.scanner.setSelectedColor(self.comboColor.currentIndex())
        self.scanner.setSelectedResolution(self.comboResolution.currentIndex())
        self.scanner.setSelectedScanArea(self.comboArea.currentIndex())
        ext = self.scanner.extension
        args = self.scanner.getArgs()

        self.statusbar.showMessage("Scan Started")
        wait(20)
        self.process.start('scanimage', args)
        if not self.process.waitForFinished(-1) or self.process.exitCode():
            self.statusbar.showMessage("Scanning Failed !")
            return
        data = self.process.readAllStandardOutput()

        filename = self.filenameEdit.text() + ext
        # to get more accurate scanned area when A4 at 300 dpi
        if (self.scanner.crop_needed):
            image = QImage.fromData(data, ext[1:].upper())
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

# returns a list of device_info dictionares containing {'device', 'vendor', 'model'}
def get_devices():
    devices = []
    process = QProcess()
    process.start('scanimage', ['-f', '%d=>%v=>%m%n'])
    if not process.waitForFinished():
        return devices
    data = bytes(process.readAllStandardOutput()).decode("utf-8").strip()
    if data=="":
        return devices
    lines = data.split("\n")
    for line in lines:
        dev, vendor, model = line.strip().split('=>')
        devices.append({'device':dev, 'vendor':vendor.upper(), 'model':model})
    return devices

def get_backend_from_scanner_device(dev_info):
    vendor = dev_info['vendor']
    device = dev_info['device']
    if vendor.upper=="HEWLETT-PACKARD":
        return HpScanner(device)
    if vendor=="CANON":
        return CanonScanner(device)
    if vendor=="EPSON":
        return EpsonScanner(device)
    if vendor=="BROTHER":
        return BrotherScanner(device)
    return DummyScanner(device)


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
