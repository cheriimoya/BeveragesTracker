class Entry:
    def __init__(self, entry_id, name, owes_total, drinks, payments):
        self.entry_id = str(entry_id)
        self.name = name
        self.owes_total = owes_total
        self.drinks = drinks
        self.payments = payments


def from_database(data_manager, person_names, person_owes):
    entries_list = []

    entries = data_manager.select('entries')

    all_beverages = [bev[1] for bev in data_manager.select(
            'beverages')]

    # select sum(amount) from entries where person_id = 11 and beverage_id = 1
    for person_id, person in enumerate(person_names):
        drinks = {}
        payments = {}
        beverage_count = []

        # to correct the index for the database
        person_id += 1

        distinct_beverages = [bev[0] for bev in data_manager.select(
            'entries',
            'DISTINCT beverage_id',
            f'is_payment = 0 AND person_id = {person_id}')]

        for bev_id in distinct_beverages:
            beverage_count.append(int(data_manager.select(
                'entries',
                'SUM(amount)',
                where=f'is_payment = 0 and person_id = {person_id} and beverage_id = {bev_id}')[0][0]))

        db_payments = data_manager.select(
            'entries',
            'timestamp, payment_value',
            where=f'is_payment = 1 and person_id = {person_id}')
        for payment in db_payments:
            payments[f'payment_{int(payment[0].timestamp())}'] = payment[1]

        for index, bev in enumerate(distinct_beverages):
            drinks[all_beverages[bev-1]] = beverage_count[index]

        entries_list.append(Entry(
            person_id,
            person,
            person_owes[person_id-1],
            drinks,
            payments))

    return entries_list


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
