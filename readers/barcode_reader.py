from readers.reader import Reader


class BarcodeReader(Reader):
    def get_id(self):
        id = int(input('Please provide identifier: '))
        return id
