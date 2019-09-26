from pdb import set_trace

from tkinter import Tk, TclError

from gui import Application
from beverages_tracker import BeveragesTracker


def main():
    bev = BeveragesTracker(tcp_reader=True)
    root = Tk()
    app = Application(backend=bev, master=root)
    try:
        while True:
            root.update()
            person_id = bev.no_wait_for_and_return_id()
            if person_id is None:
                continue
            app.active = True
            app.id_var.set(person_id)
            app.name_var.set(bev.get_person_name_by_id(person_id))
    except KeyboardInterrupt:
        pass
    except TclError:
        pass
    finally:
        for reader in bev.readers:
            reader.shutdown()


if __name__ == '__main__':
    main()
