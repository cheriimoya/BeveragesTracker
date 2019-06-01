from threading import Thread


class BarcodeReader(Thread):
    def __init__(self, parent):
        super().__init__()
        self.running = True
        self.parent = parent

    def run(self):
        while self.running:
            try:
                id = int(input('Please provide identifier: '))
            except:
                continue
            self.parent.enqueue_read((self.parent.READER_BARCODE, id))

    def shutdown(self):
        self.running = False
