# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect

engine = create_engine("postgres://obcayovm:ItiplxDZiHmnUo_7WdFtv3M67FcW1sCM@hattie.db.elephantsql.com:5432/obcayovm")



# create the application object
app = Flask(__name__)
app.secret_key = 'my precious'
# use decorators to link the function to a url
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def home():
    return render_template('index.html')  # render a template

@app.route('/welcome/')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/client_registration/', methods=['GET', 'POST'])
# @login_required
def client_registration():
    if request.method == 'POST':
        print(request.form['Name'])
    return render_template('client_registration.html')  # render a template


with engine.connect() as con:
    res_logins = con.execute('SELECT * FROM logins')
    login_ids = []
    passwords = []
    logins = []

    for val in res_logins:
        logins.append(val.values()[1])
        passwords.append(val.values()[2])
# route for handling the login page logic
@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            if (request.form['username'] in logins) & (passwords[logins.index(request.form['username'])] == request.form['password']):
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('home'))
            else:  error = 'Invalid Credentials. Please try again.'
        except Exception:
            error = 'There has been an error. Try again?'
        # if request.form['username'] not in logins or request.form['password'] != 'admin':
        #
        # else:
        #     return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('welcome'))

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)