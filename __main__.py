from pdb import set_trace

from tkinter import Tk, TclError

from gui import Application
from beverages_tracker import BeveragesTracker


def main():
    bev = BeveragesTracker(
            barcode_reader=False,
            nfc_reader=True,
            tcp_reader=False)
    root = Tk()
    app = Application(backend=bev, master=root)
    try:
        while True:
            root.update()
            id = bev.no_wait_for_and_return_id()
            if id is None:
                continue
            app.active = True
            app.id_var.set(id)
    except KeyboardInterrupt:
        pass
    except TclError:
        pass
    finally:
        for reader in bev.readers:
            reader.shutdown()


if __name__ == '__main__':
    main()
