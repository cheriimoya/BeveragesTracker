import json
from time import sleep
from pdb import set_trace
import plotTotal as pT
import entries as et
import urllib.request

from data_manager import DataManager

WEBSERVER_PATH = 'http://192.168.1.21:8000/'


def main():
    owe_list_old = []

    data_manager = DataManager()

    running = True

    while(running):
        try:
            # get users from database
            db_users = data_manager.select('users', 'name, owes')
            db_users_owe = [user[1] for user in db_users]
            db_users = [user[0] for user in db_users]

        except Exception as e:
            print(e)
            # TODO log this
            print('cannot connect to database')

        id_list = et.from_database(data_manager, db_users, db_users_owe)
        owe_list = [obj.owes_total for obj in id_list]

        # check after sleep if list is new
        if owe_list != owe_list_old:
            # plot facts
            pT.plot_liter_sum(id_list)
            pT.plot_payed_sum(id_list)
            pT.plot_debt_sum(id_list)
            pT.plot_bottles_sum(id_list)
            pT.plot_bottles_sum(id_list, 'Spezi')
            pT.plot_bottles_sum(id_list, 'Oettinger Limo')

            # plot graph for specific drinks
            pT.plot_specific_drink(id_list, 'Oetti Export')
            pT.plot_specific_drink(id_list, 'Kaffee')

            # plot graph for liters
            pT.plot_liters(id_list)
            pT.plot_liters_detailed(id_list)

            # plot graph for total owes
            pT.plot_total_owe_list(id_list)

            # plot pie graph
            pT.plot_pie(id_list)

            # set new list to old list
            owe_list_old = owe_list
        else:
            sleep(5)


if __name__ == '__main__':
    main()
