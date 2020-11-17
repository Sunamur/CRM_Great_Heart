from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash, abort
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

@main_blueprint.route('/users/', methods=['GET', 'POST'])
@login_required
def users_table():
    fields = [('login', 'Логин'),
              ('name', 'Имя'), 
              ('surname', 'Фамилия'), 
              ('birth_date', 'Дата рождения'),
              ('city', 'Город'),
              ('phone_personal', 'Телефон для связи'),
              ('work_place', 'Место основной работы'),
              ('position', 'Профессия'),
              ('position_fund', 'Позиция в фонде')]
    with db.connect() as con:
        query = con.execute("""select login, name, surname, birth_date, city, phone_personal, 
                        work_place, position, position_fund from users""")
        table = query.fetchall()
        id_query = con.execute("""select id from users""")
        ids = [str(x[0]) for x in id_query.fetchall()]

    return render_template('base_table.html', values=fields, who='сотрудников', margin_left=-10, 
                            db_table=table, ids=ids, where_to="/user_registration/", whom="сотрудника",
                            zip=zip)

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


def get_people_info(uid, table='clients'):
    qry = f'select id from {table} where id={uid}'
    with db.connect() as con:
        q_r = con.execute(qry)
        client_id = q_r.first()
        if client_id == None:
            return None
        res = con.execute(f'select * from {table} where id={uid}').first().values()
        return res


@main_blueprint.route('/user_registration/')
@login_required
def user_registration():
    fields = [('login', 'hummel', 'Логин', True),
              ('name', "Иван", 'Имя', True), 
              ('surname', "Иванов", 'Фамилия', True), 
              ('birth_date', "01-01-2020", 'Дата рождения', True),
              ('city', 'Междуречье', 'Город', True),
              ('phone_personal', "+7-800-555-35-35", 'Телефон для связи', True),
              ('email_personal', "ivanov_ivan@mail.ru", 'Email', False),
              ('tg_id', "@pupa_and_lupa", 'Контакт в Телеграм', False),
              ('phone_work', "+7-999-999-99-99", 'Дополнительный телефон для связи', False),
              ('work_place', "Хлебохладокомбинат", 'Место основной работы', True),
              ('position', "Тракторист", 'Профессия', True),
              ('position_fund', "Волонтёр", 'Позиция в фонде', True),
              ('education', "Высшее", 'Образование', False),
              ('education_minor', "Курсы по Dota 2", 'Доп. образование', False),
              ('languages', "Хорватский, польский", 'Знание языков', False),
              ('hobbies', "Любит писать CRM за еду", 'Хобби', False),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]

    return render_template('base_registration.html', values=fields, who='сотрудника', registrated_to='/user_registrated/')

@main_blueprint.route('/user_registrated/', methods=['POST'])
@login_required
def user_registrated():
    if request.method == 'POST':
        vals = request.form.to_dict()
        user_dict = {}

        for (key, value) in vals.items():
            # Check if key is even then add pair to new dictionary
            if (value != '') :
                user_dict[key] = value

        cols = list(user_dict.keys())
        cols = ", ".join(list(cols))
        vals = list(user_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        vals = ", ".join(list(vals))
        q = f'''
        Insert into users ({cols})
        values ({vals})
        '''
        with db.connect() as con:
            con.execute(q)

    return redirect('/users')


@main_blueprint.route('/users/<int:uid>/', methods=['GET'])
@login_required
def user_card(uid):
    user_data = get_people_info(uid, 'users')
    fields = [
        ('id','ID'),
        ('login','Логин'),
        ('name', 'Имя', ),
        ('surname',  'Фамилия', ),
        ('birth_date',  'Дата рождения', ),
        ('city', 'Город'),
        ('phone_personal',  'Основной телефон для связи', ),
        ('email_personal',  'Email', ),
        ('tg_id', 'Контакт в Телеграм', ),
        ('phone_work', 'Дополнительный телефон для связи', ),
        ('work_place',  'Место основной работы', ),
        ('position','Профессия', ),
        ('position_fund','Позиция в фонде', ),
        ('education', 'Образование', ),
        ('education_minor', 'Доп. образование', ),
        ('languages',  'Знание языков', ),
        ('hobbies', 'Хобби', ),
        ('comment', 'Комментарий', ),
        ('created_at','Создано'),
        ('updated_at', 'Обновлено'),
        ('is_active', 'Активен')
    ]

    if user_data is None:
        abort(404)
    if len(fields)!=len(user_data): 
        print(user_data)
        abort(500)
    payload = [[fieldname,pretty_name,data] for [fieldname,pretty_name],data in zip(fields, user_data)]
    name = ' '.join([user_data[1], user_data[2]])

    return render_template('base_card.html', values=payload, name=name, kind='User', 
            edit_page='/users/edit/' + str(uid) + '/', table_page='/users/')

@main_blueprint.route('/users/edit/<int:uid>/', methods=['GET', 'POST'])
@login_required
def user_edit(uid):
    user_data = get_people_info(uid, 'users')
    fields = [('name', user_data[2], 'Имя', True), 
              ('surname', user_data[3], 'Фамилия', True), 
              ('birth_date', user_data[4], 'Дата рождения', True),
              ('city', user_data[5], 'Город', True),
              ('phone_personal', user_data[6], 'Основной телефон для связи', True),
              ('email_personal', user_data[7], 'Email', False),
              ('tg_id', user_data[8], 'Контакт в Телеграм', False),
              ('phone_work', user_data[9], 'Дополнительный телефон для связи', False),
              ('work_place', user_data[10], 'Место основной работы', False),
              ('position', user_data[11], 'Профессия', False),
              ('position_fund', user_data[12], 'Позиция в фонде', False),
              ('education', user_data[13], 'Образование', False),
              ('education_minor', user_data[14], 'Доп. образование', False),
              ('languages', user_data[15], 'Знание языков', False),
              ('hobbies', user_data[16], 'Хобби', False),
              ('comment', user_data[17], 'Комментарий', False)]

    if user_data is None:
        abort(404)

    return render_template('base_edit.html', values=fields, who='сотруднике', 
                edit_to="/users/edited/" + str(uid) + '/', delete_to='/users/delete/' + str(uid) + '/')

@main_blueprint.route('/users/edited/<int:uid>/', methods=['POST'])
@login_required
def user_edited(uid):

    if request.method == 'POST':
        vals = request.form.to_dict()
        user_dict = {}

        for (key, value) in vals.items():
            # Check if key is even then add pair to new dictionary
            if (value != '') :
                user_dict[key] = value

        cols = list(user_dict.keys())
        # cols = ", ".join(list(cols))
        vals = list(user_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        # vals = ", ".join(list(vals))
        q = 'update users set '
        for i,j in zip(cols, vals):
            print(type(j))
            print(j == '\'None\'')
            if j != '\'None\'':
                q += f'{i} = {j},'

        q = q[:-1]
        q += f' where id = {uid}'
        with db.connect() as con:
            con.execute(q)

    return redirect(url_for('main.users_table'))

@main_blueprint.route('/users/delete/<int:uid>/', methods=['GET', 'POST'])
@login_required
def user_delete(uid):
    
    # Тут SQL запрос на удаление персонажа

    return redirect('/users/')