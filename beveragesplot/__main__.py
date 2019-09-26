import json
import time
import plotTotal as pT
import entries as et
import urllib.request


def main():
    owe_list_old = []

    while(1):
        try:
            with urllib.request.urlopen("http://192.168.1.21:8000/entries.json") as url:
                entries = json.loads(url.read().decode())
        except:
            entries = []

        id_list = et.get_entries(entries)

        owe_list = [obj.owes_total for obj in id_list]

        if owe_list != owe_list_old and bool(entries) is True:
            if 'plt' in locals():
                plt.close()

            plt = pT.plotTotal(id_list)

            plt.show(block=False)
            plt.pause(3)

            owe_list_old = owe_list
        else:
            time.sleep(5)


if __name__ == '__main__':
    main()
