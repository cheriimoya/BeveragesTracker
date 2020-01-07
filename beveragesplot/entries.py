class Entry:
    def __init__(self, entry_id, name, owes_total, drinks, payments):
        self.entry_id = str(entry_id)
        self.name = name
        self.owes_total = owes_total
        self.drinks = drinks
        self.time_list = []
        self.owes_list = []
        self.payments = payments


def from_json(entries, persons):
    entries_list = []
    for entry_id, value in entries.items():
        drinks = {}
        payments = {}
        name = 'unknown'

        for persons_id in persons:
            if str(persons_id['id']) == entry_id:
                name = persons_id['name']

        for timestamp in value:
            if timestamp == "owes_total":
                continue
            if timestamp.startswith('payment_'):
                payments[timestamp] = value[timestamp]
                continue
            for drink in value[timestamp]:
                if drink not in drinks:
                    drinks[drink] = 0
                drinks[drink] += value[timestamp][drink]
        entries_list.append(Entry(entry_id, name, value['owes_total'], drinks, payments))
    return entries_list
