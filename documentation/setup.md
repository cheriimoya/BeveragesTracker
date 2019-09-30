Setup
===
For the RFID reader setup have a look at [this guide](https://tutorials-raspberrypi.de/raspberry-pi-rfid-rc522-tueroeffner-nfc/)

| RF522 Modul | Raspberry Pi           |
|-------------|------------------------|
| SDA         | Pin 24 / GPIO8 (CE0)   |
| SCK         | Pin 23 / GPIO11 (SCKL) |
| MOSI        | Pin 19 / GPIO10 (MOSI) |
| MISO        | Pin 21 / GPIO9 (MISO)  |
| IRQ         | —                      |
| GND         | Pin 6 (GND)            |
| RST         | Pin 22 / GPIO25        |
| 3.3V        | Pin 1 (3V3)            |

![schematics](https://tutorials-raspberrypi.de/wp-content/uploads/Raspberry-Pi-RFID-RC522-NFC_Steckplatine-600x391.png)

Architecture