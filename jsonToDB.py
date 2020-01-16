import json
from pdb import set_trace

from data_manager import DataManager

data_manager = DataManager()

with open('data/persons.json') as persons:
    persons_json = json.load(persons)
with open('data/beverages.json') as beverages:
    beverages_json = json.load(beverages)
with open('data/entries.json') as entries:
    entries_json = json.load(entries)

for person in persons_json:
    data_manager.execute_query(
            'INSERT INTO users (last_id, name)\
            VALUES (%s, %s)',
            (person['id'], person['name']))
    for card in person['nfc_cards']:
        data_manager.execute_query(
            'INSERT INTO cards (id, card_owner_id)\
            VALUES (%s, (SELECT id FROM users\
            WHERE last_id = %s))',
            (card, person['id']))

for beverage in beverages_json:
    data_manager.execute_query(
            'INSERT INTO beverages (name, price)\
            VALUES (%s, %s)',
            (beverage['name'], beverage['price']))

result = data_manager.execute_query('SELECT * FROM beverages')

beverage_id = {}
for item in result:
    beverage_id[item[1]] = item[0]

for person_last_id, person_data in entries_json.items():
    data_manager.execute_query(
            'UPDATE users SET owes = %s WHERE last_id = %s',
            (person_data['owes_total'], person_last_id))
    person_id = data_manager.execute_query(
            'SELECT id FROM users WHERE last_id = %s',
            (person_last_id,))[0][0]

    for timestamp, timestamp_data in person_data.items():
        if timestamp == 'owes_total':
            continue
        if timestamp.startswith('payment_'):
            data_manager.execute_query(
                    'INSERT INTO entries \
                    (timestamp, person_id, is_payment, payment_value)\
                    VALUES (FROM_UNIXTIME(%s), %s, %s, %s)',
                    (timestamp.split('_')[1], person_id, 1, timestamp_data))
            continue

        for drink, amount in timestamp_data.items():
            data_manager.execute_query(
                    'INSERT INTO entries \
                    (timestamp, person_id, beverage_id, amount)\
                    VALUES (FROM_UNIXTIME(%s), %s, %s, %s)',
                    (timestamp, person_id, beverage_id[drink], amount))
