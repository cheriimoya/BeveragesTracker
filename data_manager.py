from pdb import set_trace
from configparser import ConfigParser
from os import environ

from mysql.connector import MySQLConnection


class DataManager():
    def __init__(self):
        self.db_config = read_db_config()
        self.ensure_tables_exist()
        if 'BEV_DEV' in environ and environ['BEV_DEV']:
            self.insert_mock_data()

    def __del__(self):
        '''
        This is the destructor. It is just used to close the
        database connection gracefully
        '''
        # TODO is this really working?
        # self.connection.close()
        if 'connection' in dir(self):
            self.connection.close()

    def ensure_tables_exist(self):
        '''
        Ensure that the needed tables exist in the database
        '''
        self.execute_query(
                "CREATE TABLE IF NOT EXISTS `users` (\
                    `id` INT AUTO_INCREMENT PRIMARY KEY,\
                    `name` VARCHAR(30) NOT NULL,\
                    `last_id` INT DEFAULT NULL,\
                    `owes` DOUBLE DEFAULT 0.0)")
        self.execute_query(
                "CREATE TABLE IF NOT EXISTS `cards` (\
                    `id` VARCHAR(12) PRIMARY KEY,\
                    `card_owner_id` INT NOT NULL)")
        self.execute_query(
                "CREATE TABLE IF NOT EXISTS `beverages` (\
                    `id` INT AUTO_INCREMENT PRIMARY KEY,\
                    `name` VARCHAR(20) NOT NULL UNIQUE,\
                    `price` FLOAT NOT NULL)")
        self.execute_query(
                "CREATE TABLE IF NOT EXISTS `entries` (\
                    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,\
                    `timestamp` TIMESTAMP,\
                    `person_id` INT NOT NULL,\
                    `is_payment` TINYINT DEFAULT 0,\
                    `beverage_id` INT,\
                    `amount` INT,\
                    `payment_value` FLOAT DEFAULT NULL)")

    def insert_mock_data(self):
        '''
        For development only, inserts mock data to the database if it is empty
        '''
        if 'BEV_DEV' in environ and environ['BEV_DEV']:
            return

        result = self.execute_query('SELECT * FROM users')
        if len(result) != 0:
            return

        mock_names = ['peter', 'horst', 'günther']
        mock_cards = ['10000000001', '23456789012', '34567890123']
        mock_drinks = [['Mate', 0.8], ['Spezi', 0.7]]

        for name in mock_names:
            self.execute_query("INSERT INTO users (name) values (%s)", (name,))
        for index, card in enumerate(mock_cards):
            self.execute_query(
                "INSERT INTO cards (id, card_owner_id)\
                values (%s, %s)", (card, index+1))

        for drink in mock_drinks:
            self.execute_query("INSERT INTO beverages (name, price)\
                    values (%s, %s)", (drink[0], drink[1]))

    def insert(self, table, columns, values):
        self.execute_query(
            f'INSERT INTO {table} ({columns}) \
            VALUES ({"%s, " * (len(columns.split(","))-1)} %s)',
            values)

    def select(self, table, columns=None, where=None):
        # TODO sql injection possible here
        return self.execute_query(
            f'SELECT {"*" if not columns else columns} FROM \
            {table} {"" if not where else "WHERE " + where}')

    def update(self, table, column, value, where):
        # TODO fix this, this is broken, column should be a sting
        # and can therefore not be 1
        assert(len(column) == 1 and len(value) == 1)
        self.execute_query(
            f'UPDATE {table} SET {column} = {value} \
            WHERE {where}')

    def execute_query(self, query, values=None):
        '''
        Makes a database query
        :param query: sql query as string
        :param values: tuple for substitution of placeholders in query string
        :return: fetchall of cursor if query is a select statement,
        None otherwise
        '''
        try:
            connection = MySQLConnection(**self.db_config)
            cursor = connection.cursor()
            if not values:
                cursor.execute(query)
            else:
                cursor.execute(query, values)
            result = None
            if query.startswith('SELECT') or query.startswith('select'):
                result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        except Exception as e:
            print(e)
            set_trace()

    def get_beverage_values(self):
        '''
        Get and return the beverages from the database
        :return: list of dicts containing name and price of bev
        '''
        beverages_as_json = []
        result = self.execute_query('SELECT name, price FROM beverages')
        for row in result:
            beverages_as_json.append({'name': row[0], 'price': row[1]})
        return beverages_as_json

    def get_person_name_by_id(self, person_id):
        '''
        Retrieve the name of a given id from the database
        :param person_id: the id to retrieve the name to
        :return: the name in case there is one, None otherwise
        '''
        result = self.execute_query(
                "SELECT name FROM users WHERE id = %s", (person_id,))
        if len(result) != 1:
            set_trace()
            return None
        return result[0][0]

    def get_person_id_by_card_uid(self, card_uid):
        '''
        Return the id of the owner of this card
        :param card_uid: the uid of the card to query
        :return: the id of the owner if found, None otherwise
        '''
        result = self.execute_query(
                "SELECT card_owner_id FROM cards where id = %s", (card_uid,))
        if len(result) != 1:
            return None
        return result[0][0]

    def person_id_exists(self, person_id):
        '''
        Checks if a person with a given id exists
        :param person_id: the person_id to check
        :return: True if person exists, False otherwise
        '''
        result = self.execute_query(
                "SELECT * FROM users WHERE id = %s",
                (person_id,))
        return len(result) == 1

    def book_transaction(self, person_id, beverages):
        '''
        Book a transaction in the database
        :param person_id:
        :param beverages: list of dicts
        '''
        if not self.person_id_exists(person_id):
            # TODO log this
            raise Exception(f'person {person_id} not found for transaction')
            return

        # this sums up all price values in the dict
        total_price = sum([float(bev['price']) for bev in beverages])

        # TODO think of a better way of updating
        owes = self.execute_query(
                'SELECT owes FROM users WHERE id = %s',
                (person_id,))[0][0]
        self.execute_query(
                'UPDATE users SET owes = %s WHERE id = %s',
                (round(total_price + owes, 2), person_id))

        # so this is a hacky bit... it sums up all drinks so we get a list
        # of how many of each unique drink kind
        unique_drinks = {}
        for drink in set([b['name'] for b in beverages]):
            unique_drinks[drink] = len(
                    [bev for bev in beverages if bev['name'] == drink])

        for beverage in unique_drinks.items():
            self.add_entry(person_id, beverage)

    def add_entry(self, person_id, beverage):
        '''
        This function adds one row to the entries table
        :param person_id: obvious
        :param beverage: tuple with name and number of beverage to add
        '''
        beverage_id = self.execute_query('SELECT id FROM beverages\
                WHERE name = %s', (beverage[0],))[0][0]
        self.execute_query(
                'INSERT INTO entries (person_id, beverage_id, amount)\
                values (%s, %s, %s)',
                (person_id, beverage_id, beverage[1]))


def read_db_config(filename='config.ini', section='mysql'):
    '''
    Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    '''
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file')
    return db
