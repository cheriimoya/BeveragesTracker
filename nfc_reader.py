from threading import Thread

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522


class NfcReader(Thread):
    def __init__(self, parent):
        super().__init__()
        self.running = True
        self.parent = parent
        self.reader = SimpleMFRC522()

    def run(self):
        while self.running:
            try:
                card_id = self.reader.read_id()
                # TODO BEEEP! let the user know card has been read
            except:
                # TODO log this
                continue
            self.parent.enqueue_read(card_id)
        GPIO.cleanup()

    def shutdown(self):
        self.running = False
