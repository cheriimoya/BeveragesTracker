from queue import Queue
from threading import Thread
from time import sleep

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
                id = self.reader.read_id()
            except:
                continue
            self.parent.enqueue_read((self.parent.READER_NFC, id))
            sleep(2)

    def shutdown(self):
        self.running = False
        GPIO.cleanup()
