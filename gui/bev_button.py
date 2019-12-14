# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/bev_button.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets

SIZE_POLICY = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Minimum,
        QtWidgets.QSizePolicy.Minimum)


class BeverageButton(QtWidgets.QPushButton):
    def setupUi(self):
        self.setObjectName("bev_button")
        self.setSizePolicy(SIZE_POLICY)
