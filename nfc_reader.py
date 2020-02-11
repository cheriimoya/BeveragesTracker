from threading import Thread
from os import environ
from time import sleep


class NfcReader(Thread):
    def __init__(self, parent):
        '''
        The constructor of the nfc reader. If the environment variable
        'BEV_DEV' is set to a non false value, this reader will continuously
        'read' the card id 10000000001 for development and/or debugging
        purposes. When 'BEV_DEV' is set, no real nfc reader hardware nor GPIO
        pins are needed.
        :param parent: the beverages tracker instance (needed for enqueue_read)
        '''
        super().__init__()
        self.running = True
        self.parent = parent
        if 'BEV_DEV' not in environ or not environ['BEV_DEV']:
            from mfrc522 import SimpleMFRC522
            self.reader = SimpleMFRC522()

    def run(self):
        '''
        If alive, try to read nfc data. When nfc data is read, the id of the
        card will be enqueued in the parent data queue for further processing.
        '''
        sleep(2)
        while self.running:
            if 'BEV_DEV' not in environ or not environ['BEV_DEV']:
                try:
                    card_id = self.reader.read_id()
                    # TODO BEEEP! let the user know card has been read
                except:
                    # TODO log this
                    continue
            else:
                card_id = '10000000001'
            self.parent.enqueue_read(card_id)
        if 'BEV_DEV' not in environ or not environ['BEV_DEV']:
            import RPi.GPIO as GPIO
            GPIO.cleanup()

    def shutdown(self):
        '''
        Shuts down the reader
        '''
        self.running = False
