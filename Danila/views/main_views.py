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

@main_blueprint.route('/users/', methods=['GET', 'POST'])
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
    with db.connect() as con:
        query = con.execute("""select name, surname, birth_date, city, phone_personal, phone_work,
                                 work_place, position_fund, education, education_minor, languages,
                                 tg_id, email_personal, position, hobbies, comment from users""")
        table = query.fetchall()
    return render_template('base_table.html', values=fields, who='членов', margin_left=-200, 
                            db_table=table, where_to="/user_registration", whom="члена", where='/users/')

@main_blueprint.route('/sponsors/', methods=['GET', 'POST'])
@login_required
def sponsors_table():
    fields = [('name', 'Имя/название'), 
              ('phone', 'Контактный телефон'),
              ('email', 'Email'),
              ('payment_details', 'Реквизиты'),
              ('socials', 'Социальные сети'),
              ('website', 'Сайт'),
              ('category', 'Тип'),
              ('comment', 'Комментарий'),]
    with db.connect() as con:
        query = con.execute("""select name, phone, email, payment_details, socials, website, category, comment from sponsors""")
        table = query.fetchall()
    return render_template('base_table.html', values=fields, who='спонсоров', margin_left=0, 
                            db_table=table, where_to="/sponsor_registration", whom="спонсора", where='/sponsors/')

@main_blueprint.route('/slaves/', methods=['GET', 'POST'])
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
    with db.connect() as con:
        query = con.execute("""select name, surname, birth, diagnosis, condition, 
                                phone_main, phone_secondary, tg_id, email, position, hobbies, comment from clients""")
        table = query.fetchall()
    return render_template('base_table.html', values=fields, who='подопечных', margin_left=0,
                            db_table=table, where_to="/client_registration", whom="подопечного")  # render a template

@main_blueprint.route('/partners/', methods=['GET', 'POST'])
@login_required
def partners_table():
    fields = [('name', 'Имя/название'), 
              ('phone', 'Контактный телефон'),
              ('email', 'Email'),
              ('payment_details', 'Реквизиты'),
              ('socials', 'Социальные сети'),
              ('website', 'Сайт'),
              ('comment', 'Комментарий'),]

    with db.connect() as con:
        query = con.execute("""select name, phone, email, payment_details, socials, website, comment from partners""")
        table = query.fetchall()
    return render_template('base_table.html', values=fields, who='партнёров', margin_left=0, 
                            db_table=table, where_to="/partner_registration", whom="партнёра")  # render a template

@main_blueprint.route('/benefactors/', methods=['GET', 'POST'])
@login_required
def benefactors_table():
    fields = [('name', 'Имя'), 
              ('surname', 'Фамилия'),
              ('birth_date', 'Дата рождения'),
              ('phone', 'Контактный телефон'),
              ('tg_id', 'Контакт в Телеграм'),
              ('email', 'Email'),
              ('socials', 'Социальные сети'),
              ('website', 'Сайт'),
              ('financial_details', 'Финансовые поступления'),
              ('comment', 'Комментарий'),]

    with db.connect() as con:
        query = con.execute("""select name, surname, birth_date, phone, tg_id, email, socials, website, financial_details, comment from benefactor""")
        table = query.fetchall()
    return render_template('base_table.html', values=fields, who='благотворителей', margin_left=0, 
                            db_table=table, where_to="/benefactor_registration", whom="благотворителя")  # render a template


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

@main_blueprint.route('/benefactor_query/', methods=['GET', 'POST'])
# @login_required
def benefactor_query():
    if request.method == 'POST':
        vals = request.form.to_dict()
        clients_query_dict = {}
        for (key, value) in vals.items():
            if (value != '') :
                clients_query_dict[key] = value
        cols = list(clients_query_dict.keys())
        cols = ", ".join(list(cols))
        vals = list(clients_query_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        vals = ", ".join(list(vals))
        # print(vals)
        benfactor_query_q = f'''
                Insert into benefactor_queries (query_timestamp, query_date, query_status_updated_at, query_coordinator, query_executor, {cols})
        values(
        now()
        , date(now())
        , now()
        , -1
        , -1
        , {vals}
        )
                '''
        with db.connect() as con:
            con.execute(benfactor_query_q)
    return render_template('benefactor_query.html')  # render a template

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


@main_blueprint.route('/clients/<int:uid>/', methods=['GET'])
@login_required
def client_card(uid):
    client_data = get_people_info(uid, 'clients')
    client_fields = [
        ["id","ID"],
        ["name","Имя"],
        ["surname","Фамилия"],
        ["birth","Дата рождения"],
        ["condition","Состояние"],
        ["diagnosis","Диагноз"],
        ["phone_main","Основной телефон"],
        ["phone_secondary","Дополнительный телефон"],
        ["tg_id","Telegram"],
        ["email","Email"],
        ["position","Статус"],
        ["hobbies","Хобби"],
        ["comment","Комментарий"],
        ["created_at","Создано"],
        ["updated_at","Обновлено"],]

    if client_data is None:
        return render_template('no user')
    if len(client_fields)!=len(client_data):
        return render_template('schema error')
    payload = [[fieldname,pretty_name,data] for [fieldname,pretty_name],data in zip(client_fields, client_data)]
    name = ' '.join([client_data[1], client_data[2]])

    return render_template('base_card.html', values=payload, name=name, kind='Client')


def get_people_info(uid, table='clients'):


    qry = f'select id from {table} where id={uid}'
    with db.connect() as con:
        q_r = con.execute(qry)
        client_id = q_r.first().values()
        if client_id == None:
            return None
        res = con.execute(f'select * from {table} where id={uid}').first().values()
        return res

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
              ('position', "Тракторист", 'Профессия', False),
              ('hobbies', "Любит писать CRM за еду", 'Хобби', False),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]

    return render_template('base_registration.html', values=fields, who='подопечного')  # render a template

@main_blueprint.route('/user_registration/', methods=['GET', 'POST'])
@login_required
def user_registration():
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
        Insert into users ({cols})
        values ({vals})
        '''
        with db.connect() as con:
            con.execute(q)

    fields = [('name', "Иван", 'Имя', True), 
              ('surname', "Иванов", 'Фамилия', True), 
              ('birth', "01-01-2020", 'Дата рождения', True),
              ('phone_personal', "+7-800-555-35-35", 'Основной телефон для связи', True),
              ('phone_work', "+7-999-999-99-99", 'Дополнительный телефон для связи', False),
              ('work_place', "Хлебохладокомбинат", 'Место основной работы', False),
              ('position_fund', "Волонтёр", 'Позиция в фонде', False),
              ('education', "Высшее", 'Образование', False),
              ('education_minor', "Курсы по Dota 2", 'Доп. образование', False),
              ('languages', "Хорватский, польский", 'Знание языков', False),
              ('tg_id', "@pupa_and_lupa", 'Контакт в Телеграм', False),
              ('email_personal', "ivanov_ivan@mail.ru", 'Email', False),
              ('position', "Тракторист", 'Профессия', False),
              ('hobbies', "Любит писать CRM за еду", 'Хобби', False),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]

    return render_template('base_registration.html', values=fields, who='подопечного')  # render a template


@main_blueprint.route('/benefactor_registration/', methods=['GET', 'POST'])
@login_required
def benefactor_registration():
    if request.method == 'POST':
        vals = request.form.to_dict()
        clients_query_dict = {}
        for (key, value) in vals.items():
            if (value != '') :
                clients_query_dict[key] = value

        cols = list(clients_query_dict.keys())
        cols.pop()
        cols = ", ".join(list(cols))
        vals = list(clients_query_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        benefactor_category = vals.pop()

        vals = ", ".join(list(vals))
        benfactor_q = f'''
                Insert into benefactor (created_at, updated_at,  {cols})
        values(
        now()
        , now()
        , {vals}
        )
                '''
        benefactor_category_q = f"""
        insert into benefactor_category (created_at, updated_at, category)
        values (now(), now(), {benefactor_category})
        """

        with db.connect() as con:
            con.execute(benfactor_q)
            con.execute(benefactor_category_q)

    fields = [('name', "Иван", 'Имя', True), 
            ('surname', "Иванов", 'Фамилия', True), 
            ('birth_date', "01-01-2020", 'Дата рождения', False),
            ('phone','+7-800-555-35-35', 'Контактный телефон', False),
            ('tg_id', '@pupa_and_lupa','Контакт в Телеграм', False),
            ('email', 'ivan_ivanov@mail.ru', 'Email', True),
            ('socials', 'Instagram: @pupa; VK: vk.com/ivan_ivanov', 'Социальные сети', False),
            ('website', 'pupa&lupa.com', 'Сайт', False),
            ('comment', 'Любит запах напалма по утрам', 'Комментарий', False),]

    return render_template('base_registration.html', values=fields, who='благотворителя')

@main_blueprint.route('/sponsor_registration/', methods=['GET', 'POST'])
@login_required
def sponsor_registration():
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
        Insert into sponsors ({cols})
        values ({vals})
        '''
        with db.connect() as con:
            con.execute(q)

    fields = [('name', "Иван/Иванов и КО", 'Имя/название', True), 
              ('phone', "+7-800-555-35-35", 'Телефон для связи', True),
              ('email', "ivanov_ivan@mail.ru", 'Email', False),
              ('socials', "Instagram: @pupa; VK: vk.com/ivan_ivanov", 'Социальные сети', False),
              ('website', "pupa&lupa.com", 'Сайт', False),
              ('category', "ВИП", 'Категория', False),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]

    return render_template('base_registration.html', values=fields, who='спонсора')

# @main_blueprint.route('/partner_registration/', methods=['GET', 'POST'])
# @login_required
# def partner_registration():
#     if request.method == 'POST':
#         vals = request.form.to_dict()
#         client_dict = {}
#
#         for (key, value) in vals.items():
#             # Check if key is even then add pair to new dictionary
#             if (value != '') :
#                 client_dict[key] = value
#
#         cols = list(client_dict.keys())
#         cols = ", ".join(list(cols))
#         vals = list(client_dict.values())
#         for i in range(len(vals)):
#             if isinstance(vals[i], str):
#                 vals[i] = "'" + vals[i] + "'"
#         vals = ", ".join(list(vals))
#         q = f'''
#         Insert into partners ({cols})
#         values ({vals})
#         '''
#         with db.connect() as con:
#             con.execute(q)
#
#     fields = [('name', "Иван/Иванов и КО", 'Имя/название', True),
#               ('phone', "+7-800-555-35-35", 'Телефон для связи', True),
#               ('email', "ivanov_ivan@mail.ru", 'Email', False),
#               ('socials', "Instagram: @pupa; VK: vk.com/ivan_ivanov", 'Социальные сети', False),
#               ('website', "pupa&lupa.com", 'Сайт', False),
#               ('category', "ВИП", 'Категория', False),
#               ('comment', "Любит ванильный кофе", 'Комментарий', False)]
#
#     return render_template('base_registration.html', values=fields, who='партнёра')


@main_blueprint.route('/partner_registration/', methods=['GET', 'POST'])
@login_required
def partner_registration():
    if request.method == 'POST':
        vals = request.form.to_dict()
        clients_query_dict = {}
        for (key, value) in vals.items():
            if (value != '') :
                clients_query_dict[key] = value

        cols = list(clients_query_dict.keys())
        # cols.pop()
        cols = ", ".join(list(cols))
        vals = list(clients_query_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        # benefactor_category = vals.pop()

        vals = ", ".join(list(vals))
        print(vals, cols)
        q = f'''
                        Insert into partners (updated_at, created_at, {cols})
                values(
                now()
                , now()
                , {vals}
                )
                        '''
        with db.connect() as con:
            con.execute(q)

    return render_template('partner_registration.html')

@main_blueprint.route('/partner_contact_info/', methods=['GET', 'POST'])
@login_required
def partner_contact_info():
    if request.method == 'POST':
        vals = request.form.to_dict()
        clients_query_dict = {}
        for (key, value) in vals.items():
            if (value != '') :
                clients_query_dict[key] = value

        cols = list(clients_query_dict.keys())
        # cols.pop()
        cols = ", ".join(list(cols))
        vals = list(clients_query_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        # benefactor_category = vals.pop()

        vals = ", ".join(list(vals))
        print(vals, cols)
    return render_template('partner_contact_info.html')