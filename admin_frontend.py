import os
from hashlib import sha512
import json
from time import time

from flask import Flask, render_template, request, session, redirect, url_for

from data_manager import DataManager

ADMIN_PASSWORD = b"\xd4\x01yHC\x88\x05\xdd3q\xc0'\x06\xbc\xc3hd\xa86\xc9 \xc9\x91\x00&*GP*\xc4\x18Y\x92<\x0c4?\x86A+\x0c\xdb^\xb9\x11[\xc6\x87\x08\xf6\xd2\x05_\xfd\x19\xd5\x91\xed\xaa\x1d0\x9b\xb0d"

app = Flask('admin_frontend')
app.secret_key = os.urandom(12)
app.debug = False

data_manager = DataManager()


@app.route('/')
def index():
    '''
    This will list all users in the database. From here users can create new
    users or update/delete existing ones.
    '''
    if 'username' not in session:
        return redirect(url_for('login'))

    last_card_id = 'no last card id'
    try:
        with open('unknown_card_id.txt') as uid_file:
            last_card_id = uid_file.read()
    except:
        pass

    try:
        persons = data_manager.select('users')
    except Exception as e:
        return render_template(
                'index.html',
                errors=e,
                last_card_id=last_card_id)

    return render_template(
            'index.html',
            users=persons,
            last_card_id=last_card_id)


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    '''
    Creates a user and insert the generated entry into the database
    '''
    if 'username' not in session:
        return redirect(url_for('login'))

    last_card_id = 'no last card id'
    try:
        with open('unknown_card_id.txt') as uid_file:
            last_card_id = uid_file.read()
    except:
        pass

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            cards = request.form.get('cards')

            if not name or not cards:
                raise Exception('name and/or cards not given')

            cards = [c for c in cards.split(',')]

            data_manager.insert(
                    'users',
                    'name',
                    (name,))
            max_id = data_manager.select(
                    'users',
                    'MAX(id)')[0][0]
            for card in cards:
                data_manager.insert(
                        'cards',
                        'id, card_owner_id',
                        (card, max_id))
        except Exception as e:
            return render_template(
                    'create_user.html',
                    last_card_id=last_card_id,
                    errors=e)
        return redirect(url_for('index'))
    return render_template(
            'create_user.html',
            last_card_id=last_card_id)


@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    '''
    Update the name or the owes value of a user.
    '''
    # TODO implement ability to update cards aswell
    if 'username' not in session:
        return redirect(url_for('login'))

    last_card_id = 'no last card id'
    try:
        with open('unknown_card_id.txt') as uid_file:
            last_card_id = uid_file.read()
    except:
        pass

    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            name = request.form.get('name')
            owes = request.form.get('owes')

            if not user_id:
                raise Exception('user id not given')

            if not name and not owes:
                raise Exception('there is nothing to change')

            # TODO this query is not injection proof
            query_string = 'UPDATE users SET '
            if name:
                query_string += f'name={name}'
            if owes:
                if name:
                    query_string += ','
                query_string += f'owes={owes}'
            query_string += ' WHERE id=%s'
            data_manager.execute_query(
                    query_string,
                    (user_id,))
        except Exception as e:
            return render_template(
                    'update_user.html',
                    last_card_id=last_card_id,
                    errors=e)
        return redirect(url_for('index'))

    try:
        # try to get the given user from the database
        user_id_get = request.args.get('user_id')

        if not user_id_get:
            raise Exception('please do not call this page without a user id')

        # TODO this query is not injection proof, id parameter
        user_id, user_name, user_last_id, user_owes = data_manager.select(
                'users',
                where=f'id={user_id_get}')[0]

        return render_template(
                'update_user.html',
                user_id=user_id,
                user_name=user_name,
                user_owes=user_owes,
                last_card_id=last_card_id)
    except Exception as e:
        return render_template(
                'update_user.html',
                last_card_id=last_card_id,
                errors=e)


@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    '''
    Delete a user with a given id.
    '''
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')

            if not user_id:
                raise Exception('user id not given')

            data_manager.execute_query(
                    'DELETE FROM users WHERE id=%s',
                    (user_id,))
            data_manager.execute_query(
                    'DELETE FROM cards WHERE card_owner_id=%s',
                    (user_id,))
            return 'deleted! <a href="/">return to index</a>'

        except Exception as e:
            return render_template(
                    'delete_user.html',
                    errors=e)
    try:
        # try to get the given user from the database
        user_id_get = request.args.get('user_id')

        if not user_id_get:
            raise Exception('please do not call this page without a user id')

        # TODO this query is not injection proof
        user_id, user_name, user_last_id, user_owes = data_manager.select(
                'users',
                where=f'id={user_id_get}')[0]

        return render_template(
                'delete_user.html',
                user_id=user_id,
                user_name=user_name,
                user_owes=user_owes)
    except Exception as e:
        return render_template(
                'delete.html',
                errors=e)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Login the user. This is the page where every other page redirects to if
    a user is not logged in.
    '''
    html = '''
        <form method="post">
        <p><input type=password name=password>
        <p><input type=submit value=Login>
        </form>
        '''
    if request.method == 'POST':
        if 'password' not in request.form:
            return html
        pw_hash = sha512(request.form['password'].encode()).digest()
        if pw_hash == ADMIN_PASSWORD:
            session['username'] = 'admin'
            return redirect(url_for('index'))
        html = f'wrong passwd<br>{html}'
    return html


@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            user_id = int(request.form.get('user_id'))
            amount = float(request.form.get('amount'))

            owes_currently = data_manager.execute_query(
                    'SELECT owes FROM users where id=%s',
                    (user_id,))[0][0]

            new_amount = round(owes_currently - amount, 2)
            data_manager.execute_query(
                    'UPDATE users SET owes = %s WHERE id = %s',
                    (new_amount, user_id))

            data_manager.execute_query(
                    'INSERT INTO \
                    entries (person_id, is_payment, payment_value)\
                    VALUES (%s, 1, %s)',
                    (user_id, amount))
        except Exception as e:
            return render_template(
                    'pay.html',
                    errors=e)
        return 'payed! <a href="/">return home</a>'

    try:
        # try to get the given user from the database
        user_id_get = request.args.get('user_id')

        if not user_id_get:
            raise Exception('please do not call this page without a user id')

        # TODO this query is not injection proof
        user_id, user_name, _, user_owes = data_manager.select(
                'users',
                where=f'id={user_id_get}')[0]
    except Exception as e:
        return render_template(
                'pay.html',
                errors=e)
    return render_template(
            'pay.html',
            user_id=user_id,
            user_name=user_name,
            user_owes=user_owes)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return '''
        oops, this was an error.
        please open an issue<br>
        error: ''' + error, 500


def run():
    app.run(port=9000, host='0.0.0.0')


if __name__ == '__main__':
    run()
