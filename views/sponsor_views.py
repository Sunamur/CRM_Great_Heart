from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash, abort
from app import db
from .main_views import get_people_info
# import pandas as pd

sponsor_blueprint = Blueprint('sponsor', __name__, template_folder='templates')



@sponsor_blueprint.route('/sponsor_registration/')
@login_required
def sponsor_registration():

    fields = [('name', "Иван/Иванов и КО", 'Имя/название', True), 
              ('payment_details', '5469 3800 5500 3322', 'Платёжные реквизиты', False),
              ('phone', "+7-800-555-35-35", 'Телефон для связи', True),
              ('email', "ivanov_ivan@mail.ru", 'Email', True),
              ('socials', "Instagram: @pupa; VK: vk.com/ivan_ivanov", 'Социальные сети', False),
              ('website', "pupa&lupa.com", 'Сайт', True),
              ('category', "ВИП", 'Категория', True),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]

    return render_template('base_registration.html', values=fields, who='спонсора', 
            registered_to="/sponsor_registered/")

@sponsor_blueprint.route('/sponsor_registered/', methods=['POST'])
@login_required
def sponsor_registered():
    if request.method == 'POST':
        vals = request.form.to_dict()
        sponsor_dict = {}

        for (key, value) in vals.items():
            # Check if key is even then add pair to new dictionary
            if (value != '') :
                sponsor_dict[key] = value

        cols = list(sponsor_dict.keys())
        cols = ", ".join(list(cols))
        vals = list(sponsor_dict.values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"
        vals = ", ".join(list(vals))
        q = f'''
        Insert into sponsors (updated_at, created_at, {cols})
        values (now(), now(), {vals})
        '''
        with db.connect() as con:
            con.execute(q)

    return redirect('/sponsors/')


@sponsor_blueprint.route('/sponsors/', methods=['GET', 'POST'])
@login_required
def sponsors_table():
    fields = [('name', 'Имя/название'), 
              ('phone', 'Контактный телефон'),
              ('email', 'Email'),
              ('website', 'Сайт'),
              ('category', 'Тип')]
    with db.connect() as con:
        query = con.execute("""select name, phone, email, website, category from sponsors""")
        table = query.fetchall()
        id_query = con.execute("""select id from sponsors""")
        ids = [str(x[0]) for x in id_query.fetchall()]

    return render_template('base_table.html', values=fields, who='спонсоров',  
                            db_table=table, ids=ids, where_to="/sponsor_registration", 
                            whom="спонсора", bp='sponsor', zip=zip)




@sponsor_blueprint.route('/sponsors/<int:uid>/', methods=['GET'])
@login_required
def sponsor_card(uid):
    data = get_people_info(uid, 'sponsors')

    fields = [
        ('id','ID'),
        ('name',  'Имя/название'), 
        ('payment_details', 'Платёжные реквизиты'),
        ('logo', 'Тут должно быть лого'),
        ('phone','Телефон для связи'),
        ('email',  'Email'),
        ('socials',  'Социальные сети'),
        ('website', 'Сайт'),
        ('category', 'Категория'),
        ('comment',  'Комментарий'),
        ('created_at','Создано'),
        ('updated_at', 'Обновлено'),
    ]

    if data is None:
        abort(404)
        # return render_template('no user')
    if len(fields)!=len(data): 
        abort(500)
    payload = [[fieldname, pretty_name,data] for [fieldname,pretty_name],data in zip(fields, data)]
    name = data[1]

    return render_template('base_card.html', values=payload, name=name, kind='Sponsor', 
            edit_page='/sponsors/edit/' + str(uid) + '/', table_page='/sponsors/')

@sponsor_blueprint.route('/sponsors/edit/<int:uid>/', methods=['GET', 'POST'])
@login_required
def sponsors_edit(uid):
    data = get_people_info(uid, 'sponsors')
    fields = [('name', data[1], 'Имя/название', True), 
              ('phone', data[4], 'Телефон для связи', True),
              ('email', data[5], 'Email', True),
              ('socials', data[6], 'Социальные сети', False),
              ('website', data[7], 'Сайт', True),
              ('category', data[8], 'Категория', True),
              ('comment', data[9], 'Комментарий', False)]

    if data is None:
        abort(404)

    return render_template('base_edit.html', values=fields, who='спонсоре', 
                edit_to="/sponsors/edited/" + str(uid) + '/')

@sponsor_blueprint.route('/sponsors/edited/<int:uid>/', methods=['POST'])
@login_required
def sponsor_edited(uid):

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
        q = 'update sponsors set '
        for i,j in zip(cols, vals):
            if j != '\'None\'':
                q += f'{i} = {j},'

        q += f'updated_at = now() where id = {uid}'
        with db.connect() as con:
            con.execute(q)

    return redirect('/sponsors/')