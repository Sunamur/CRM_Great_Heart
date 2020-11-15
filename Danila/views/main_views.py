from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash
from app import db
# import pandas as pd

main_blueprint = Blueprint('main', __name__, template_folder='templates')

@main_blueprint.route('/')
@login_required
def home():
    return render_template('index.html')

# @main_blueprint.route('/welcome/')
# def welcome():
#     return render_template('welcome.html')

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

    fields = [('name', "Иван", 'Имя', True), 
              ('surname', "Иванов", 'Фамилия', True), 
              ('birth', "01-01-2020", 'Дата рождения', True),
              ('diagnosis', "Поступил на ФТиАД", 'Диагноз', True),
              ('condition', "Учится на ФТиАД", 'Состояние', True),
              ('phone_main', "+7-800-555-35-35", 'Основной телефон для связи', True),
              ('phone_secondary', "+7-999-999-99-99", 'Дополнительный телефон для связи', False),
              ('tg_id', "@pupa_and_lupa", 'Контакт в Телеграм', False),
              ('email', "ivanov_ivan@mail.ru", 'Email', False),
              ('position', "Подрочист", 'Профессия', False),
              ('hobbies', "Любит писать CRM за еду", 'Хобби', False),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]

    return render_template('client_registration.html', values=fields)  # render a template

@main_blueprint.route('/users', methods=['GET', 'POST'])
@login_required
def users_table():
    fields = [('name', 'Имя'), 
              ('surname', 'Фамилия'), 
              ('birth_date', 'Дата рождения'),
              ('city', 'Город'),
              ('phone_personal', 'Основной телефон для связи'),
              ('phone_work', 'Дополнительный телефон для связи'),
              ('work_place', 'Место основной работы'),
              ('position_fund', 'Позиция в фонде'),
              ('education', 'Образование'),
              ('education_minor', 'Доп. образование'),
              ('languages', 'Знание языков'),
              ('tg_id', 'Контакт в Телеграм'),
              ('email_personal', 'Email'),
              ('position', 'Профессия'),
              ('hobbies', 'Хобби'),
              ('comment', 'Комментарий')]

    return render_template('users.html', values=fields)  # render a template

@main_blueprint.route('/sponsors', methods=['GET', 'POST'])
@login_required
def sponsors_table():
    return render_template('sponsors.html')  # render a template

@main_blueprint.route('/slaves', methods=['GET', 'POST'])
@login_required
def slaves_table():
    fields = [('name', 'Имя'), 
              ('surname', 'Фамилия'), 
              ('birth', 'Дата рождения'),
              ('diagnosis', 'Диагноз'),
              ('condition', 'Состояние'),
              ('phone_main', 'Основной телефон для связи'),
              ('phone_secondary', 'Дополнительный телефон для связи'),
              ('tg_id', 'Контакт в Телеграм'),
              ('email', 'Email'),
              ('position', 'Профессия'),
              ('hobbies', 'Хобби'),
              ('comment', 'Комментарий')]
    return render_template('slaves.html', values=fields)  # render a template

@main_blueprint.route('/partners', methods=['GET', 'POST'])
@login_required
def partners_table():
    return render_template('partners.html')  # render a template



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
    # flash('You were logged out.')
    return redirect(url_for('main.home'))


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