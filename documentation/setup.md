Setup
===

The hardware part
---

As mentioned in the [README.md](../README.md), regarding the hardware part of
the project, you'll need:
- a raspberry pi 3b+ or better (the project is only tested on a 3b+)
- an MFRC522 RFID reader
- seven female to female jumper wires
- a touch screen device (the best would be a touch screen attached to the pi)

### RFID reader

For the RFID reader setup have a look at [this guide](https://tutorials-raspberrypi.de/raspberry-pi-rfid-rc522-tueroeffner-nfc/)

| RF522 Module | Raspberry Pi           |
|--------------|------------------------|
| SDA          | Pin 24 / GPIO8 (CE0)   |
| SCK          | Pin 23 / GPIO11 (SCKL) |
| MOSI         | Pin 19 / GPIO10 (MOSI) |
| MISO         | Pin 21 / GPIO9 (MISO)  |
| IRQ          | —                      |
| GND          | Pin 6 (GND)            |
| RST          | Pin 22 / GPIO25        |
| 3.3V         | Pin 1 (3V3)            |

![schematics](https://tutorials-raspberrypi.de/wp-content/uploads/Raspberry-Pi-RFID-RC522-NFC_Steckplatine-600x391.png)

### Display

Soo if you have a touch screen for the raspberry... good for you!

But if you don't have money for a touchscreen, but you have an old android
tablet laying around, you can use that tablet.

Just connect the tablet to the same network that the raspberry is running on,
install a vnc server on the raspi and a client on the tablet and you're good to
go (that's what we did!).


Install and run
---

I'll assume that you are running raspbian on a raspberry pi with a working
xserver and git installed.

Needed programs/tools:
- mysql/mariadb
- python3
  - RPi
  - flask
  - matplotlib
  - mfrc522
  - numpy
  - pip
  - tkinter

Install mariadb, python3 and pip3 (use your package manager):
`sudo apt install mariadb python3 python3-pip`

Install tkinter (use your package manager):
`sudo apt install python3-tk`

Install the python libraries:
`pip3 install --user flask mfrc522 matplotlib numpy`

Clone the project:
`git clone [this repo url]`

You'll have to create a database user and a database.
Then just copy the `config.ini.example` to `config.ini` and adjust.

To start the project execute `python3 __main__.py` or just `python3 .` in the
project root. If the `BEV_DEV` variable is set to a value that evaluates to
`True` the tracker will create mock data if a database is empty.
