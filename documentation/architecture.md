Architecture
---

The `__main__.py` creates a `BeveragesTracker` object which in turn creates an
`nfc_reader` object.

The `nfc_reader` object is started in its own thread and writes all ids it
reads to the `BeveragesTracker` via a (threadsafe) queue.

After creating the `BeveragesTracker`, the `__main__.py` will create a `Tk`
root object and a tkinter `Frame` object with all the graphical contents we can
see in the picture below.

![tkinter gui](documentation/files/tkinter_gui.png)

The gui sets all the button to a `disabled` state so they are not clickable
until the tracker reads a known id.

Then the script will enter a while True loop in which it checks if there are
any new ids.  If there are, it will activate the gui panel (activate the
previously disabled buttons) and update the name of the read id.  If there was
no id read or the id could not be mapped to any person registered, nothing will
happen and the gui will stay disabled.

After clicking the buy button, the gui will tell the backend which id to charge
what amount and which drinks (shady, shady)...
