# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(413, 213)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.comboColor = QtGui.QComboBox(self.centralwidget)
        self.comboColor.setObjectName(_fromUtf8("comboColor"))
        self.comboColor.addItem(_fromUtf8(""))
        self.comboColor.addItem(_fromUtf8(""))
        self.comboColor.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboColor, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 3, 1, 1)
        self.comboResolution = QtGui.QComboBox(self.centralwidget)
        self.comboResolution.setObjectName(_fromUtf8("comboResolution"))
        self.comboResolution.addItem(_fromUtf8(""))
        self.comboResolution.addItem(_fromUtf8(""))
        self.comboResolution.addItem(_fromUtf8(""))
        self.comboResolution.addItem(_fromUtf8(""))
        self.comboResolution.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboResolution, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.comboArea = QtGui.QComboBox(self.centralwidget)
        self.comboArea.setObjectName(_fromUtf8("comboArea"))
        self.comboArea.addItem(_fromUtf8(""))
        self.comboArea.addItem(_fromUtf8(""))
        self.comboArea.addItem(_fromUtf8(""))
        self.comboArea.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboArea, 3, 2, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.scanBtn = QtGui.QPushButton(self.centralwidget)
        self.scanBtn.setObjectName(_fromUtf8("scanBtn"))
        self.gridLayout.addWidget(self.scanBtn, 5, 3, 1, 1)
        self.closeBtn = QtGui.QPushButton(self.centralwidget)
        self.closeBtn.setObjectName(_fromUtf8("closeBtn"))
        self.gridLayout.addWidget(self.closeBtn, 5, 0, 1, 1)
        self.filenameEdit = QtGui.QLineEdit(self.centralwidget)
        self.filenameEdit.setObjectName(_fromUtf8("filenameEdit"))
        self.gridLayout.addWidget(self.filenameEdit, 0, 2, 1, 1)
        self.labelExt = QtGui.QLabel(self.centralwidget)
        self.labelExt.setObjectName(_fromUtf8("labelExt"))
        self.gridLayout.addWidget(self.labelExt, 0, 3, 1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.comboResolution.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "HP Scan", None))
        self.comboColor.setItemText(0, _translate("MainWindow", "Color", None))
        self.comboColor.setItemText(1, _translate("MainWindow", "Gray", None))
        self.comboColor.setItemText(2, _translate("MainWindow", "Lineart", None))
        self.label_3.setText(_translate("MainWindow", "Resolution :", None))
        self.comboResolution.setItemText(0, _translate("MainWindow", "100 DPI", None))
        self.comboResolution.setItemText(1, _translate("MainWindow", "200 DPI", None))
        self.comboResolution.setItemText(2, _translate("MainWindow", "300 DPI", None))
        self.comboResolution.setItemText(3, _translate("MainWindow", "600 DPI", None))
        self.comboResolution.setItemText(4, _translate("MainWindow", "1200 DPI", None))
        self.label_4.setText(_translate("MainWindow", "Scan Area :", None))
        self.comboArea.setItemText(0, _translate("MainWindow", "Full Area", None))
        self.comboArea.setItemText(1, _translate("MainWindow", "4x6 inch Landscape", None))
        self.comboArea.setItemText(2, _translate("MainWindow", "Letter (8.5x11in)", None))
        self.comboArea.setItemText(3, _translate("MainWindow", "A4 (297x210mm)", None))
        self.label_2.setText(_translate("MainWindow", "Color Mode :", None))
        self.label.setText(_translate("MainWindow", "Output :", None))
        self.scanBtn.setText(_translate("MainWindow", "Scan", None))
        self.closeBtn.setText(_translate("MainWindow", "Close", None))
        self.filenameEdit.setPlaceholderText(_translate("MainWindow", "filename", None))
        self.labelExt.setText(_translate("MainWindow", "  .jpg", None))

