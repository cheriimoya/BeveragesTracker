import json
from functools import partial
from pdb import set_trace
from queue import Queue

from tkinter import Button, Frame, X, BOTH, Label, StringVar, font


class Application(Frame):
    def __init__(self, backend, master=None):
        super().__init__(master)
        self.price = 0
        self.master = master
        self.active = False
        self.fontType = font.Font(family='Helvetica', size=18)
        self.bev = backend
        self.initialize_ui()

    def initialize_ui(self):
        self.pack(fill=BOTH, expand=True)
        self.frame_list = []

        for frame in range(3):
            self.frame_list.append(Frame(self))
            self.frame_list[frame].pack(expand=True, side='left', fill=BOTH)

        for item in self.get_beverage_values():
            fun = partial(self.add_to_temp_list, item)
            btn = Button(
                    self.frame_list[0],
                    text=f"{item['name']}: {item['price']}",
                    font=self.fontType,
                    width=1,
                    command=fun)
            btn.pack(fill=X, side="top")

        self.price_var = StringVar()
        self.price_var.set('0.00 €')
        self.price_label = Label(
                self.frame_list[1],
                textvariable=self.price_var,
                font=self.fontType,
                bg='grey')
        self.price_label.pack(fill=X, side='bottom')

        self.id_var = StringVar()
        self.name_var = StringVar()
        self.id_var.set('0')
        self.name_var.set('-name-')
        self.id_label = Label(
                self.frame_list[2],
                font=self.fontType,
                textvariable=self.name_var)
        self.id_label.pack(side='top')

        buy = Button(
                self.frame_list[2],
                text="BUY",
                fg="green",
                font=self.fontType,
                command=self.book_transaction)
        buy.pack(expand=True, side='top', fill=BOTH)

        quit = Button(
                self.frame_list[2],
                text="QUIT",
                fg="red",
                font=self.fontType,
                command=self.master.destroy)
        quit.pack(side="bottom")

    # TODO: export to helper function
    def get_beverage_values(self):
        try:
            with open('data/beverages.json') as bevs:
                return json.loads(bevs.read())
        except Exception as e:
            print(e)
            set_trace()
            return {}

    def add_to_temp_list(self, item):
        if not self.active:
            return
        Entry(self.frame_list[1], self, item)
        self.calculate_and_display_total()

    def remove_from_temp_list(self, entry):
        entry.destroy()
        self.calculate_and_display_total()

    def calculate_and_display_total(self):
        sum = 0
        for entry in self.frame_list[1].winfo_children()[1:]:
            sum += float(entry.price)
        self.price_var.set(f'{round(sum, 2):.2f} €')
        self.price = sum

    def book_transaction(self):
        if not self.active:
            return
        items = []
        for child in self.frame_list[1].winfo_children()[1:]:
            items.append(child.item)
            child.destroy()
        self.bev.update_beverages_for_id(self.id_var.get(), items)
        self.name_var.set('-name-')
        self.calculate_and_display_total()
        self.active = False


class Entry(Frame):
    def __init__(self, master, controller, item):
        super().__init__(master)
        self.price = item['price']
        self.item = item

        self.name = Label(
                self,
                font=controller.fontType,
                text=item['name'])
        self.name.pack(side='left')

        self.price_label = Label(
                self,
                font=controller.fontType,
                text=item['price'])
        self.price_label.pack(side='left')

        fun = partial(controller.remove_from_temp_list, self)
        self.delete_button = Button(
                self,
                text='X',
                font=controller.fontType,
                command=fun)
        self.delete_button.pack(side='right')

        self.pack(side='top', fill=X)
