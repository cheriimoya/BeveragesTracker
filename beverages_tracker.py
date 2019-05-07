import json


class BeveragesTracker:

    def __init__(self):# {{{
        self.running = True
        self.entries = self.load_data()# }}}

    def start_loop(self):# {{{
        try:
            while self.running:
                id = self.read_id()
                self.update_amount_for_id(id)
                print('Updated: ' + str(self.entries))
                self.save_data()

        except KeyboardInterrupt:
            pass
        finally:
            self.save_data()# }}}

    def read_id(self):# {{{
        id = None
        while id is None:
            try:
                id = int(input('Please provide identifier: '))
                break
            except KeyboardInterrupt as abort:
                raise abort
            except:
                pass
        return str(id)# }}}

    def update_amount_for_id(self, id):# {{{
        if id not in self.entries:
            self.entries[id] = 0
        self.entries[id] += 1# }}}

    def save_data(self):# {{{
        with open('entries.json', 'w') as save_file:
            save_file.write(json.dumps(self.entries))# }}}

    def load_data(self):# {{{
        try:
            with open('entries.json') as entries:
                return json.loads(entries.read())
        except:
            return json.loads('{}')# }}}
