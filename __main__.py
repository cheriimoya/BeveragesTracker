import json

def main():
    running = True

    entries = load_data()

    try:
        while running:
            id = read_id()
            update_amount_for_id(entries, id)
            print('Update: ' + str(entries))
            save_data(entries)

    except KeyboardInterrupt:
        pass
    finally:
        save_data(entries)

def read_id():
    id = None
    while id is None:
        try:
            id = int(input('Please give me your Matrikelnummer: '))
            break
        except KeyboardInterrupt as abort:
            raise abort
        except:
            pass
    return str(id)

def update_amount_for_id(entries, id):
    if id not in entries:
        entries[id] = 0

    entries[id] += 1
    return entries[id]

def save_data(entries):
    with open('entries.json', 'w') as save_file:
        save_file.write(json.dumps(entries))

def load_data():
    jentries = {}
    with open('entries.json') as entries:
        jentries = json.loads(entries.read())
    return jentries

if __name__ == '__main__':
    main()
