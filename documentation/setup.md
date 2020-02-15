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

In this project we used a MFRC522 RFID reader. If you want to read NFC cards like MIFARE DESFire you need to modify your reader as mentioned in [MFRC522.md](./MFRC522.md) or just buy a KKmoon PN532 or any other 
reader which is able to apply more than 3,3 V.
Because all NFC cards need a certain strength of the electromagnetic field to properly activate and exchange their data. The MFRC522 reader only applys ~3,3 V this is enough for NFC cards like MIFARE Classic
but cards like the MIFARE DESFire need ~5 V to get activated and exchange. Thats why we need to modify our reader to get 5 V support.

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
