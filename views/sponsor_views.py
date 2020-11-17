from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash, abort
from app import db
from .main_views import get_people_info
# import pandas as pd

sponsor_blueprint = Blueprint('sponsor', __name__, template_folder='templates')



@sponsor_blueprint.route('/sponsor_registration/', methods=['GET', 'POST'])
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

    return render_template('base_registration.html', values=fields, who='спонсора', back_to="/sponsors/")



@sponsor_blueprint.route('/sponsors/', methods=['GET', 'POST'])
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
        id_query = con.execute("""select id from sponsors""")
        ids = [str(x[0]) for x in id_query.fetchall()]

    return render_template('base_table.html', values=fields, who='спонсоров', margin_left=0, 
                            db_table=table, ids=ids, where_to="/sponsor_registration", whom="спонсора", bp='sponsor', zip=zip)




@sponsor_blueprint.route('/sponsors/<int:uid>/', methods=['GET'])
@login_required
def client_card(uid):
    data = get_people_info(uid, 'sponsors')

    fields = [
        ('id','ID'),
        ('name',  'Имя/название'), 
        ('payment_details', 'Платежные детали'),
        ( 'logo', 'Лого'),
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
    payload = [[fieldname,pretty_name,data] for [fieldname,pretty_name],data in zip(fields, data)]
    name =data[2]

    return render_template('base_card.html', values=payload, name=name, kind='Sponsor')
