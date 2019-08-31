BeveragesTracker
===

This small project can be used to track who is taking beverages (or any other
kind of countable items).

It is using integer identifiers, so it can be used with some sort of
student/employee id or just some random numbers.

At the moment, the implementation only increments a number associated with
the given identifier, therefore it is very (veeerryyy) basic.

For the RFID reader setup have a look at [this guide](https://tutorials-raspberrypi.de/raspberry-pi-rfid-rc522-tueroeffner-nfc/)

| RF522 Modul | Raspberry Pi           |
|-------------|------------------------|
| SDA         | Pin 24 / GPIO8 (CE0)   |
| SCK         | Pin 23 / GPIO11 (SCKL) |
| MOSI        | Pin 19 / GPIO10 (MOSI) |
| MISO        | Pin 21 / GPIO9 (MISO)  |
| IRQ         | —                      |
| GND         | Pin6 (GND)             |
| RST         | Pin22 / GPIO25         |
| 3.3V        | Pin 1 (3V3)            |

---

Ideas for TODOs:
---
- Add pretty statistics
- Add webserver to get information
- Add different multipliers for calculating prices and stuff
- Make project more modular, so ids can also be obtained with NFC tags, ...

- Always: Fix bugs
