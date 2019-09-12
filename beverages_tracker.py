import json
from queue import Queue, Empty
from time import time
from pdb import set_trace

import person

READER_BARCODE = 1
READER_NFC = 2
READER_TCP = 3


class BeveragesTracker:
    def __init__(self, barcode_reader=False, nfc_reader=False, tcp_reader=False):
        '''The init function tries to load data from a file called entries.json
        and persons.json in the project root.
        If no readers are set, the program will exit without doing anything.'''
        self.running = True
        self.entries = self.load_data()
        self.persons = self.load_persons()
        self.read_queue = Queue()
        self.readers = []
        if barcode_reader:
            from barcode_reader import BarcodeReader
            self.barcode_reader = BarcodeReader(self, READER_BARCODE)
            self.readers.append(self.barcode_reader)
        if nfc_reader:
            from nfc_reader import NfcReader
            self.nfc_reader = NfcReader(self, READER_NFC)
            self.readers.append(self.nfc_reader)
        if tcp_reader:
            from tcp_reader import TCPReader
            self.tcp_reader = TCPReader(self, READER_TCP)
            self.readers.append(self.tcp_reader)
        for reader in self.readers:
            reader.start()

    def enqueue_read(self, data):
        (kind, id) = data
        if kind is READER_NFC:
            person = self.get_person_by_card_uid(id)
            if person is None:
                # TODO: log this
                print('Person not registered yet!')
                return
            id = person.id
        self.read_queue.put(id)

    def start_loop(self):
        try:
            while self.running:
                id = self.read_queue.get()
                self.update_amount_for_id(str(id))
                # TODO: log that
                print('Updated: ' + str(self.entries))
                self.save_data()
        except KeyboardInterrupt:
            for reader in self.readers:
                reader.shutdown()
        finally:
            self.save_data()


    def update_beverages_for_id(self, id, beverages):
        # TODO: add user properly
        if id not in self.entries or type(self.entries[id]) != dict:
            self.entries[id] = {'owes_total': 0.0}
        owes = 0.0

        timestamp = int(time())
        if timestamp not in self.entries[id]:
            self.entries[id][timestamp] = {}
        for beverage in beverages:
            if beverage['name'] not in self.entries[id][timestamp]:
                self.entries[id][timestamp][beverage['name']] = 0
            self.entries[id][timestamp][beverage['name']] += 1
            owes += float(beverage['price'])
        self.entries[id]['owes_total'] += owes
        self.save_data()

    def update_amount_for_id(self, id):
        '''Increases the count for a given id by one'''
        if id not in self.entries:
            self.entries[id] = 0
        self.entries[id] += 1

    def get_person_by_card_uid(self, id):
        '''Return person that a given id belongs to.
        If the id is not registered yet, this function will
        return None'''
        for person in self.persons:
            if person.has_nfc_id(id):
                return person

    def save_data(self):
        '''This function saves the volatile data as json into a file called
        entries.json in the current directory.'''
        with open('entries.json', 'w') as save_file:
            save_file.write(json.dumps(self.entries))

    def load_data(self):
        '''This function loads the entries.json file.
        If it doesn't exist, it just returns an empty json array.'''
        try:
            with open('entries.json') as entries:
                return json.loads(entries.read())
        except:
            return json.loads('{}')

    def load_persons(self):
        '''Loads and returns persons.json from the current directory.
        If this file does not exist an empty array will be
        returned.'''
        try:
            with open('persons.json') as persons_file:
                js = json.loads(persons_file.readline())
                persons = person.from_json(js)
                return persons
        except:
            return json.loads('[]')

    def save_persons(self):
        '''Save all entries to persons.json in the current
        directory.'''
        try:
            with open('persons.json', 'w') as persons_file:
                persons_file.writelines(json.dumps(self.persons))
        except:
            # TODO: also log this
            print('Failed to write persons to file!')
