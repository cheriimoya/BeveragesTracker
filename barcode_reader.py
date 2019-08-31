from reader import Reader


class BarcodeReader(Reader):
    get_id(self):
        id = int(input('Please provide identifier: '))
        self.parent.enqueue_read((self.reader_id, id))


    def shutdown(self):
        self.running = False
