from tkinter import Tk, TclError

from gui import Application
from beverages_tracker import BeveragesTracker


def main():
    bev = BeveragesTracker()
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
            app.name_var.set(bev.data_manager.get_person_name_by_id(person_id))
    except KeyboardInterrupt:
        root.destroy()
    except TclError:
        pass
    finally:
        bev.nfc_reader.shutdown()


if __name__ == '__main__':
    main()
