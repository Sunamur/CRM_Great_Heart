from functools import wraps
from flask import redirect, url_for, flash, session

def get_login_info(db):
    with db.connect() as con:
        res_logins = con.execute('SELECT * FROM logins')
        passwords = []
        logins = []

        for val in res_logins:
            logins.append(val.values()[1])
            passwords.append(val.values()[2])
    return logins, passwords


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('main.login'))
    return wrap
