import json
import random


class Entries:

    def __init__(self, name):
        self.name = str(name)
        self.owes_total = 0
        self.drink_list = []
        self.time_list = []
        self.owes_list = []

    def get_name(self):
        return self.name

    def get_owes_total(self):
        return self.owes_total

    def get_drink_list(self):
        return self.drink_list

    def get_time_list(self):
        return self.time_list

    def get_owes_list(self):
        return self.owes_list

    def set_owes_total(self, value):
        self.owes_total = value

    def set_drink_list(self, value):
        self.drink_list = value

    def set_time_list(self, value):
        self.time_list = value

    def set_owes_list(self, value):
        self.owes_list = value


def get_entries(entries):
    idList = []
    owesList = []
    i = 0

    for id in entries:
        idList.append(Entries(id))
        print(id)
        for timestamp in entries[id]:
            if timestamp == "owes_total":
                idList[i].set_owes_total(entries[id][timestamp])

        idList[i].set_owes_list(owesList)
        owesList = []
        i += 1

    return idList
