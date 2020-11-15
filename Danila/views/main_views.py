from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash
from app import db
import pandas as pd

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
@login_required
def home():
    return render_template('index.html')

@main_blueprint.route('/welcome/')
def welcome():
    return render_template('welcome.html')

@main_blueprint.route('/client_registration/', methods=['GET', 'POST'])
@login_required
def client_registration():
    if request.method == 'POST':
        vals = request.form.to_dict()
        client_dict = {}

        for (key, value) in vals.items():
            # Check if key is even then add pair to new dictionary
            if (value != '') :
                client_dict[key] = value

        cols = list(client_dict.keys())
        cols = ", ".join(list(cols))
        vals = list(client_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        vals = ", ".join(list(vals))
        q = f'''
        Insert into clients ({cols})
        values ({vals})
        '''
        with db.connect() as con:
            con.execute(q)

    return render_template('client_registration.html')  # render a template



@main_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            logins, passwords = get_login_info(db)
            if (request.form['username'] in logins) & (passwords[logins.index(request.form['username'])] == request.form['password']):
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('main.home'))
            else:  error = 'Invalid Credentials. Please try again.'
        except Exception as e:

            error = f'There has been an error: {e}. Try again?'

    return render_template('login.html', error=error)

@main_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('main.welcome'))


@main_blueprint.route('/client_query/', methods=['GET', 'POST'])
# @login_required
def client_query():
    if request.method == 'POST':
        vals = request.form.to_dict()
        clients_query_dict = {}
        for (key, value) in vals.items():
            # Check if key is even then add pair to new dictionary
            if (value != '') :
                clients_query_dict[key] = value

        cols = list(clients_query_dict.keys())
        cols = ", ".join(list(cols))
        vals = list(clients_query_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        vals = ", ".join(list(vals))
        id = f"""select id from clients where phone_main = cast('{request.form['phone']}' as varchar)"""
        client_id = -1
        q = f'''
                Insert into clients_queries (query_date, query_timestamp, query_status_updated_at, query_executer, query_coordinator, client_id, {cols})
        values(
        date(now())
        , now()
        , now()
        , 1
        , 1
        , {client_id}
        , {vals}
        )
                '''
        with db.connect() as con:
            q_r = con.execute(id)
            client_id = q_r.first().values()
            if client_id != None:
                client_id = client_id[0]
            else:
                client_id = -1
            con.execute(q)
    return render_template('client_query.html')  # render a template

@main_blueprint.route('/all_client_queries/', methods=['GET', 'POST'])
def all_client_queries():
    with db.connect() as con:
        queries = con.execute('select * from clients_queries')
    keys = queries.keys()
    vals = []

    for row in queries:
        vals.append(row.values())
    df = pd.DataFrame(vals, columns = keys)
    df.to_html('/Users/danilaukader/CRM_Great_Heart/Danila/templates/all_client_queries.html')
    return render_template('all_client_queries.html')