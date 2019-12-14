import sys
import json
from pdb import set_trace
from functools import partial

from PyQt5 import QtWidgets

from gui.custom_frame import DrinkLine
from gui.main_window import Ui_MainWindow
from gui.bev_button import BeverageButton

SIZE_POLICY = QtWidgets.QSizePolicy(
        QtWidgets.QSizePolicy.Minimum,
        QtWidgets.QSizePolicy.Minimum)


def get_beverage_values():
    try:
        with open('data/beverages.json') as bevs:
            return json.load(bevs)
    except Exception as e:
        print("Could not load file:", e)
        return [{"name": "test", "price": "6"}]


class UI():
    def __init__(self, MainWindow):
        self.active = True
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.drink_list = []
        self.setup_ui()

    def setup_ui(self):
        for bev in get_beverage_values():
            button = BeverageButton()
            button.setText(f'{bev["name"]}: {bev["price"]}')
            button.setSizePolicy(SIZE_POLICY)
            fun = partial(self.add_to_temp_list, bev)
            button.clicked.connect(fun)
            self.ui.vertical1.addWidget(button)

    def add_to_temp_list(self, item):
        if not self.active:
            return
        self.ui.drinks_list.addWidget(DrinkLine(self, item))
        self.calculate_and_display_total()

    def remove_from_temp_list(self, entry):
        entry.setParent(None)
        self.calculate_and_display_total()

    def calculate_and_display_total(self):
        sum = 0
        print('----')
        for index in range(self.ui.drinks_list.count()):
            print(index, self.ui.drinks_list.itemAt(index).widget().y())
        #     sum += float(entry.price)
        # self.price_var.set(f'{round(sum, 2):.2f} €')
        # self.price = sum

# def book_transaction(self):
#     if not self.active:
#         return
#     items = []
#     for child in self.frame_list[1].winfo_children()[1:]:
#         items.append(child.item)
#         child.destroy()
#     if len(items) > 0:
#         self.bev.update_beverages_for_id(self.id_var.get(), items)
#     self.name_var.set('-name-')
#     self.calculate_and_display_total()
#     self.active = False
#
#
# def cancel_transaction(self):
#     if not self.active:
#         return
#     for child in self.frame_list[1].winfo_children()[1:]:
#         child.destroy()
#     self.name_var.set('-name-')
#     self.calculate_and_display_total()
#     self.active = False
#
#
# class Entry(Frame):
#     def __init__(self, master, controller, item):
#         super().__init__(master)
#         self.price = item['price']
#         self.item = item
#
#         self.name = Label(
#                 self,
#                 font=controller.fontType,
#                 text=item['name'])
#         self.name.pack(side='left')
#
#         self.price_label = Label(
#                 self,
#                 font=controller.fontType,
#                 text=item['price'])
#         self.price_label.pack(side='left')
#
#         fun = partial(controller.remove_from_temp_list, self)
#         self.delete_button = Button(
#                 self,
#                 text='X',
#                 font=controller.fontType,
#                 command=fun)
#         self.delete_button.pack(side='right')
#
#         self.pack(side='top', fill=X)


class Ui_drink_line(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.label_drink_name = None


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    UI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
