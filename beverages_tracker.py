from queue import Queue, Empty

from data_manager import DataManager


class BeveragesTracker:
    def __init__(self):
        '''
        The init function tries to load data from a file called entries.json
        and persons.json in the data folder within the project root. It then
        starts a nfc_reader thread.
        '''
        self.running = True
        self.data_manager = DataManager()
        self.read_queue = Queue()
        from nfc_reader import NfcReader
        self.nfc_reader = NfcReader(self)
        self.nfc_reader.start()

    def enqueue_read(self, card_id):
        '''
        This will find out the id of the owner of a card and enque the read.
        If there is no card owner, this will do nothing.
        :param card_id: the id of the card
        :return: nothing
        '''
        person_id = self.get_person_id_by_card_uid(card_id)
        if not person_id:
            return
        self.read_queue.put(person_id)

    def no_wait_for_and_return_id(self):
        '''
        Return id if it is available, None if it is not
        '''
        try:
            return self.read_queue.get_nowait()
        except Empty:
            return None

    def update_beverages_for_id(self, person_id, beverages):
        '''
        Add the data contained in 'beverages' to person_id
        :param person_id: id of the person
        :param beverages: list of dicts
        '''
        # TODO: add user properly
        self.data_manager.book_transaction(person_id, beverages)

    def get_person_id_by_card_uid(self, card_uid):
        '''
        Return person that a given id belongs to.  If the id is not
        registered yet, this function will write the uid to a file called
        unknown_card_id.txt and return None
        :param card_uid: pretty obvious
        :return: person_id
        '''
        result = self.data_manager.get_person_id_by_card_uid(card_uid)
        if result:
            return result

        # TODO: log this
        print('Person not registered yet!')
        with open('unknown_card_id.txt', 'w') as uid_file:
            uid_file.write(str(card_uid))
