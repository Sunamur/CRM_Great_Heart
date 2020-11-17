from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash, abort
from app import db
from .main_views import get_people_info
# import pandas as pd

benefactor_blueprint = Blueprint('benefactor', __name__, template_folder='templates')



@benefactor_blueprint.route('/benefactors/', methods=['GET', 'POST'])
@login_required
def benefactors_table():
    fields = [('name', 'Имя'), 
              ('surname', 'Фамилия'),
              ('email', 'Email'),]

    with db.connect() as con:
        query = con.execute("""select name, surname, email from benefactor""")
        table = query.fetchall()
        id_query = con.execute("""select id from benefactor""")
        ids = [str(x[0]) for x in id_query.fetchall()]
    return render_template('base_table.html', values=fields, who='благотворителей',  
                            db_table=table, ids=ids, where_to="/benefactor_registration", 
                            whom="благотворителя", zip=zip) 




@benefactor_blueprint.route('/benefactor_query/', methods=['GET', 'POST'])
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
        benefactor_query_q = f'''
        Insert into benefactor_queries (query_timestamp, query_date, query_status_updated_at, query_coordinator, query_executor, {cols})
        values(now(), date(now()), now(), -1, -1, {vals})
        '''
        with db.connect() as con:
            con.execute(benefactor_query_q)
    return render_template('benefactor_query.html')  # render a template



@benefactor_blueprint.route('/benefactor_registration/', methods=['GET', 'POST'])
@login_required
def benefactor_registration():

    fields = [('name', "Иван", 'Имя', True), 
              ('surname', "Иванов", 'Фамилия', True), 
              ('birth_date', "01-01-2020", 'Дата рождения', False),
              ('phone','+7-800-555-35-35', 'Контактный телефон', False),
              ('tg_id', '@pupa_and_lupa','Контакт в Телеграм', False),
              ('email', 'ivan_ivanov@mail.ru', 'Email', True),
              ('socials', 'Instagram: @pupa; VK: vk.com/ivan_ivanov', 'Социальные сети', False),
              ('website', 'pupa&lupa.com', 'Сайт', False),
              ('financial_details', '500', 'Финансовые поступления', False),
              ('comment', 'Любит запах напалма по утрам', 'Комментарий', False),]

    return render_template('base_registration.html', values=fields, who='благотворителя', 
            registered_to="/benefactor_registered/")

@benefactor_blueprint.route('/benefactor_registered/', methods=['GET', 'POST'])
@login_required
def benefactor_registered():
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
        benefactor_category = vals.pop()

        vals = ", ".join(list(vals))
        benefactor_q = f'''
        Insert into benefactor (created_at, updated_at, {cols})
        values(now(), now(), {vals})
        '''
        benefactor_category_q = f"""
        insert into benefactor_category (created_at, updated_at, category)
        values (now(), now(), {benefactor_category})
        """

        with db.connect() as con:
            con.execute(benefactor_q)
            con.execute(benefactor_category_q)

    return redirect('/benefactors/')


@benefactor_blueprint.route('/benefactors/<int:uid>/', methods=['GET'])
@login_required
def benefactor_card(uid):
    data = get_people_info(uid, 'benefactor')
    fields = [('id', 'ID'),
              ('name', 'Имя'), 
              ('surname', 'Фамилия'),
              ('birth_date', 'Дата рождения'),
              ('phone', 'Контактный телефон'),
              ('tg_id', 'Контакт в Телеграм'),
              ('email', 'Email'),
              ('socials', 'Социальные сети'),
              ('website', 'Сайт'),
              ('financial_details', 'Финансовые поступления'),
              ('comment', 'Комментарий'),
              ('created_at','Создано'),
              ('updated_at', 'Обновлено'),]

    if data is None:
        abort(404)
    if len(fields)!=len(data):
        abort(500)
    payload = [[fieldname,pretty_name,data] for [fieldname,pretty_name],data in zip(fields, data)]
    name = ' '.join([data[1], data[2]])

    return render_template('base_card.html', values=payload, name=name, kind='Benefactor',
            edit_page='/benefactors/edit/' + str(uid) + '/', table_page='/benefactors/')

@benefactor_blueprint.route('/benefactors/edit/<int:uid>/', methods=['GET', 'POST'])
@login_required
def benefactor_edit(uid):
    data = get_people_info(uid, 'benefactor')
    fields = [('name', data[1], 'Имя', True), 
              ('surname', data[2], 'Фамилия', True), 
              ('birth_date', data[3], 'Дата рождения', False),
              ('phone', data[4], 'Контактный телефон', False),
              ('tg_id', data[5],'Контакт в Телеграм', False),
              ('email', data[6], 'Email', True),
              ('socials', data[7], 'Социальные сети', False),
              ('website', data[8], 'Сайт', False),
              ('comment', data[9], 'Комментарий', False),
              ('financial_details', data[10], 'Финансовые поступления', False)]

    if data is None:
        abort(404)

    return render_template('base_edit.html', values=fields, who='благотворителе', 
                edit_to="/benefactors/edited/" + str(uid) + '/')

@benefactor_blueprint.route('/benefactors/edited/<int:uid>/', methods=['POST'])
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
        q = 'update benefactor set '
        for i,j in zip(cols, vals):
            if j != '\'None\'':
                q += f'{i} = {j},'

        q += f'updated_at = now() where id = {uid}'
        with db.connect() as con:
            con.execute(q)

    return redirect('/benefactors/')