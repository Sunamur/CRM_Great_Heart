from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash, abort
from app import db
from .main_views import get_people_info
# import pandas as pd
client_blueprint = Blueprint('client', __name__, template_folder='templates')



@client_blueprint.route('/client_query/', methods=['GET', 'POST'])
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



@client_blueprint.route('/all_client_queries/', methods=['GET', 'POST'])
def all_client_queries():
    with db.connect() as con:
        queries = con.execute('select * from clients_queries')
        id_query = con.execute("""select id from clients_queries""")
        ids = id_query.fetchall()
    keys = queries.keys()
    vals = []

    for row in queries:
        vals.append(row.values())


    return render_template('base_table.html', values=list(zip(keys, keys)), who='обращений клиентов', margin_left=-200, 
                            db_table=vals, ids=ids, where_to="/client_query", whom="обращение", zip=zip)



@client_blueprint.route('/client_registration/', methods=['GET', 'POST'])
@login_required
def client_registration():

    fields = [('name', "Иван", 'Имя', True), 
              ('surname', "Иванов", 'Фамилия', True), 
              ('birth', "01-01-2020", 'Дата рождения', False),
              ('condition', "Учится на ФТиАД", 'Состояние', True),
              ('diagnosis', "Поступил на ФТиАД", 'Диагноз', True),
              ('phone_main', "+7-800-555-35-35", 'Телефон для связи', True),
              ('phone_secondary', "+7-999-999-99-99", 'Доп. телефон для связи', False),
              ('tg_id', "@pupa_and_lupa", 'Контакт в Телеграм', False),
              ('email', "ivanov_ivan@mail.ru", 'Email', False),
              ('position', "Тракторист", 'Профессия', False),
              ('hobbies', "Любит писать CRM за еду", 'Хобби', False),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]

    return render_template('base_registration.html', values=fields, who='подопечного', registered_to="/client_registered/")  # render a template

@client_blueprint.route('/client_registered/', methods=['GET', 'POST'])
@login_required
def client_registered():
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

    return redirect('/clients')

@client_blueprint.route('/clients/<int:uid>/', methods=['GET'])
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
        abort(404)
        # return render_template('no user')
    if len(client_fields)!=len(client_data):
        abort(500)
    payload = [[fieldname,pretty_name,data] for [fieldname,pretty_name],data in zip(client_fields, client_data)]
    name = ' '.join([client_data[1], client_data[2]])

    return render_template('base_card.html', values=payload, name=name, kind='Client', 
            edit_page="/clients/edit/" + str(uid) + '/', table_page='/clients/')

@client_blueprint.route('/clients/edit/<int:uid>/', methods=['GET', 'POST'])
@login_required
def client_edit(uid):
    client_data = get_people_info(uid, 'clients')
    fields = [('name', client_data[1], 'Имя', True), 
              ('surname', client_data[2], 'Фамилия', True), 
              ('birth', client_data[3], 'Дата рождения', False),
              ('condition', client_data[4], 'Состояние', True),
              ('diagnosis', client_data[5], 'Диагноз', True),
              ('phone_main', client_data[6], 'Телефон для связи', True),
              ('phone_secondary', client_data[7], 'Доп. телефон для связи', False),
              ('tg_id', client_data[8], 'Контакт в Телеграм', False),
              ('email', client_data[9], 'Email', False),
              ('position', client_data[10], 'Профессия', False),
              ('hobbies', client_data[11], 'Хобби', False),
              ('comment', client_data[12], 'Комментарий', False)]

    if client_data is None:
        abort(404)

    return render_template('base_edit.html', values=fields, who='подопечного', 
            edit_to="/clients/edited/" + str(uid) + '/')

@client_blueprint.route('/clients/edited/<int:uid>/', methods=['POST'])
@login_required
def client_edited(uid):

    if request.method == 'POST':
        vals = request.form.to_dict()
        client_dict = {}

        for (key, value) in vals.items():
            # Check if key is even then add pair to new dictionary
            if (value != '') :
                client_dict[key] = value

        cols = list(client_dict.keys())
        # cols = ", ".join(list(cols))
        vals = list(client_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        # vals = ", ".join(list(vals))
        q = 'update clients set '
        for i,j in zip(cols, vals):
            if j != '\'None\'':
                q += f'{i} = {j},'

        q = q[:-1]
        q += f' where id = {uid}'
        with db.connect() as con:
            con.execute(q)
    

    return redirect('/clients/')

@client_blueprint.route('/clients/', methods=['GET', 'POST'])
@login_required
def clients_table():
    fields = [('name', 'Имя'), 
              ('surname', 'Фамилия'), 
              ('condition', 'Состояние'),
              ('diagnosis', 'Диагноз'),
              ('phone_main', 'Основной телефон для связи'),]
    with db.connect() as con:
        query = con.execute("""select name, surname, diagnosis, condition, 
                                phone_main from clients""")
        table = query.fetchall()
        id_query = con.execute("""select id from clients""")
        ids = [str(x[0]) for x in id_query.fetchall()]

    return render_template('base_table.html', values=fields, who='подопечных', 
            db_table=table, ids=ids, where_to="/client_registration", 
            whom="подопечного", bp='client', zip=zip) 
