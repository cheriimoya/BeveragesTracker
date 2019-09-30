import os
from hashlib import sha512
import json

from flask import Flask, render_template, request, session, redirect, url_for

ADMIN_PASSWORD = b"\xd4\x01yHC\x88\x05\xdd3q\xc0'\x06\xbc\xc3hd\xa86\xc9 \xc9\x91\x00&*GP*\xc4\x18Y\x92<\x0c4?\x86A+\x0c\xdb^\xb9\x11[\xc6\x87\x08\xf6\xd2\x05_\xfd\x19\xd5\x91\xed\xaa\x1d0\x9b\xb0d"

app = Flask('admin_frontend')
app.secret_key = os.urandom(12)
app.debug = False


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    with open('data/entries.json') as entries_file:
        entries = json.dumps(json.load(entries_file), indent=4)
    with open('data/persons.json') as persons_file:
        persons = json.dumps(json.load(persons_file), indent=4)
    try:
        with open('unknown_card_id.txt') as uid_file:
            last_card_id = uid_file.read()
    except:
        last_card_id = 'no last card id'
    if request.method == 'POST':
        try:
            new_entries = request.form.get('entries')
            new_persons = request.form.get('persons')
            # remove \n and \r plus validify correctness of json
            new_entries = json.loads(new_entries)
            new_persons = json.loads(new_persons)
            update_backend(
                    entries=new_entries,
                    persons=new_persons)
        except Exception as e:
            return render_template(
                    'index.html',
                    entries=json.dumps(new_entries, indent=4),
                    persons=json.dumps(new_persons, indent=4),
                    last_card_id=last_card_id,
                    errors=e)
        return redirect(url_for('index'))
    return render_template(
            'index.html',
            entries=entries,
            persons=persons,
            last_card_id=last_card_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    html = '''
        <form method="post">
        <p><input type=password name=password>
        <p><input type=submit value=Login>
        </form>
        '''
    if request.method == 'POST':
        pw_hash = sha512(request.form['password'].encode()).digest()
        if pw_hash == ADMIN_PASSWORD:
            session['username'] = 'admin'
            return redirect(url_for('index'))
        html = f'wrong passwd<br>{html}'
    return html


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


def update_backend(entries=None, persons=None):
    assert entries is not None
    assert persons is not None

    with open('data/entries.json', 'w') as entries_file:
        json.dump(entries, entries_file, indent=4)
    with open('data/persons.json', 'w') as persons_file:
        json.dump(persons, persons_file, indent=4)


def run():
    app.run(port=9000, host='0.0.0.0')


if __name__ == '__main__':
    run()
