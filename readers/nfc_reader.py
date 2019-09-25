from time import sleep

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

from readers.reader import Reader


class NfcReader(Reader):
    def __init__(self, parent, reader_id):
        super().__init__(parent, reader_id)
        self.reader = SimpleMFRC522()

    def get_id(self):
        try:
            id = self.reader.read_id()
            # BEEEP! let the user know card has been read
        except:
            raise
        sleep(1)
        return id

    def shutdown(self):
        self.running = False
        GPIO.cleanup()
