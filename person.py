class Person():
    def __init__(self, id, name, nfc_ids=[]):
        assert(type(id) is int)
        self.id = id
        self.name = name
        self.nfc_ids = nfc_ids

    def has_nfc_id(self, id):
        return id in self.nfc_ids


def from_json(json):
    persons = []
    for item in json:
        p = Person(int(item['id']), item['name'], item['nfc_cards'])
        persons.append(p)
    return persons


if __name__ == '__main__':
    print('Please do not run this module directly')
