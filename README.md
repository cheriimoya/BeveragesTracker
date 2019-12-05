BeveragesTracker
===

This project can be used to track the consumption of beverages (or any other
kind of countable items).

It uses a Raspberry pi 3b+ and an MFRC522 RFID NFC chip.

The Android tablet is only providing a touch frontend with via a vnc client and
we wouldn't need it if we had a touchscreen unit for the pi (the latency would
also be better).

Here is a little demo:
![demo video](documentation/files/demo_video.mp4)

It is using arbitrary identifiers, so it can be used with any sort of
student/employee id or just some random numbers.

Afterwards you can analyze the data, e.g. find out what item is consumed the
most, or who is in how much debt.

Requirements
---

- Raspberry pi 3B+ or better
- RFID-RC522 chip
- some display, if possible, a touchscreen

Setup
---

For setup instructions have a look at
[the setup guide](documentation/setup.md).

Statistics Display
---

Render 'pretty' statistics! For examples and how to set it up, read
[this](documentation/statistics_display.md)

Admin frontend
---

Have a look at
[the admin frontend markdown file](documentation/admin_frontend.md).

Architecture
---

If you are interested in the architecture of the project (and how bad it really
is), take a look at [this](documentation/architecture.md)

Bad decisions
---

Currently the project uses tkinter as frontend. This was probably a bad
decision as it is really unflexible and doesn't work well with threading.

The data is stored in json files, which was probably also a bad decision, as
they don't scale well.

Probably the project is too flexible. There can be several readers in parallel,
reading and providing ids like crazy.  But i'm not too sure if this makes much
sense... The nfc reader is probably the only reader the project needs. The tcp
reader was only for development and the barcode reader was implemented because
i was still waiting for the nfc reader `¯\_(ツ)_/¯`

COULDDOs:
---

- [ ] rewrite frontend in PyQt5
- [ ] add moar pretty statistics
- [ ] move from json files to a database
- [ ] move admin panel to the front end (activated via card id)
  - [ ] create user from the admin panel
  - [ ] inventory management within the admin panel

- Always: Fix bugs
