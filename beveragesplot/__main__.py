import json
from time import sleep
from pdb import set_trace
import plotTotal as pT
import entries as et
import urllib.request

WEBSERVER_PATH = 'http://192.168.1.21:8000/'


def main():
    owe_list_old = []

    while(True):
        try:
            with urllib.request.urlopen(
                    WEBSERVER_PATH + "entries.json") as json_entries:
                entries = json.loads(json_entries.read().decode())
            with urllib.request.urlopen(
                    WEBSERVER_PATH + "persons.json") as json_persons:
                persons = json.loads(json_persons.read().decode())
        except:
            entries = []
            persons = []

        id_list = et.from_json(entries, persons)
        owe_list = [obj.owes_total for obj in id_list]

        if owe_list != owe_list_old and entries:
            if 'plt' in locals():
                plt.close()

            plt = pT.plotTotal(id_list, persons)

            plt.show(block=False)
            plt.pause(3)

            owe_list_old = owe_list
        else:
            sleep(5)


if __name__ == '__main__':
    main()
