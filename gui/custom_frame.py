from functools import partial

from PyQt5 import QtWidgets


class DrinkLine(QtWidgets.QWidget):
    def __init__(self, parent, item):
        super().__init__(parent.ui.centralwidget)
        self.item = item

        self.horizontalLayout = QtWidgets.QHBoxLayout(self)

        textline = QtWidgets.QLabel(self)
        textline.setText(
                f'{item["name"]} - {item["price"]}')
        self.horizontalLayout.addWidget(textline)

        removeItemButton = QtWidgets.QPushButton(self)
        removeItemButton.setText('X')
        fun = partial(parent.remove_from_temp_list, self)
        removeItemButton.clicked.connect(fun)
        self.horizontalLayout.addWidget(removeItemButton)
