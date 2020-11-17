from auth import login_required, get_login_info
from flask import redirect, render_template, Blueprint, request, session, url_for, flash, abort
from app import db
from .main_views import get_people_info

partner_blueprint = Blueprint('partner', __name__, template_folder='templates')



@partner_blueprint.route('/partners/', methods=['GET', 'POST'])
@login_required
def partners_table():
    fields = [('type', 'Тип'),
              ('name', 'Имя/название'),
              ('inn', "ИНН"),
              ('ogrn','ОГРН'),
              ('legal_address', 'Юрридический адрес'),
              ('phone', 'Телефон для связи'),
              ('email', 'Email'),
              ('website', 'Сайт'),
              ('sphere', 'Сфера деятельности'),
              ('category',  'Категория')]

    with db.connect() as con:
        query = con.execute("""select type, name, inn, ogrn, legal_address, 
            phone, email, website, sphere, category from partners""")
        table = query.fetchall()
        id_query = con.execute("""select id from partners""")
        ids = [str(x[0]) for x in id_query.fetchall()]

    return render_template('base_table.html', values=fields, who='партнёров',  
                            db_table=table, ids=ids, where_to="/partner_registration", 
                            whom="партнёра", bp="partner", zip=zip)

@partner_blueprint.route('/partner_registration/')
@login_required
def partner_registration():

    fields = [('type', "Физическое/Юридическое", 'Тип', True),
              ('name', "Иван/Иванов и КО", 'Имя/название', True),
              ('inn', '1234567890', "ИНН", True),
              ('ogrn', '1234567890', 'ОГРН', True),
              ('legal_address', 'Сеул, улица Небытия 48', 'Юрридический адрес', True),
              ('payment_details', "ХЗ", 'Реквизиты', False),
              ('logo', "Вставляй картинку в текстовое поле", 'Лого', False),
              ('phone', "+7-800-555-35-35", 'Телефон для связи', True),
              ('email', "ivanov_ivan@mail.ru", 'Email', True),
              ('socials', "Instagram: @pupa; VK: vk.com/ivan_ivanov", 'Социальные сети', False),
              ('website', "pupa&lupa.com", 'Сайт', True),
              ('sphere', "Полиграфия", 'Сфера деятельности', True),
              ('category', "ВИП", 'Категория', True),
              ('comment', "Любит ванильный кофе", 'Комментарий', False)]
    return render_template('base_registration.html', values=fields, who='партнёра', 
        registered_to="/partner_registered/")

@partner_blueprint.route('/partner_registered/')
@login_required
def partner_registered():
    if request.method == 'POST':
        vals = request.form.to_dict()
        partner_dict = {}
        for (key, value) in vals.items():
            if (value != '') :
                partner_dict [key] = value

        cols = list(partner_dict .keys())
        # cols.pop()
        cols = ", ".join(list(cols))
        vals = list(partner_dict .values())
        for i in range(len(vals)):
            if isinstance(vals[i], str):
                vals[i] = "'" + vals[i] + "'"

        vals = ", ".join(list(vals))
        print(vals, cols)
        q = f'''
        Insert into partners (updated_at, created_at, {cols})
        values(now(), now(), {vals})
        '''
        with db.connect() as con:
            con.execute(q)

    return redirect('/partners/')


@partner_blueprint.route('/partner_contact_info/', methods=['GET', 'POST'])
@login_required
def partner_contact_info():
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
        print(vals, cols)

        q = f'''
        Insert into partners_contact_info (updated_at, created_at, start_date, {cols})
        values(now(), now(), date(now()), {vals})
        '''
        with db.connect() as con:
            con.execute(q)
    return render_template('partner_contact_info.html')


@partner_blueprint.route('/partners/<int:uid>/', methods=['GET'])
@login_required
def parnter_card(uid):
    data = get_people_info(uid, 'partners')
    fields = [('id','ID'),
              ('type',  'Тип', ),
              ('name','Имя/название', ),
              ('inn',"ИНН", ),
              ('ogrn', 'ОГРН', ),
              ('legal_address',  'Адрес', ),
              ('payment_details','Реквизиты', ),
              ('logo',  'Лого', ),
              ('phone', 'Телефон для связи', ),
              ('email','Email', ),
              ('socials', 'Социальные сети', ),
              ('website',  'Сайт', ),
              ('sphere',  'Сфера деятельности', ),
              ('category', 'Категория', ),
              ('comment',  'Комментарий', ),
              ('created_at','Создано'),
              ('updated_at', 'Обновлено'),
    ]

    if data is None:
        abort(404)
    if len(fields)!=len(data): 
        abort(500)
    payload = [[fieldname,pretty_name,data] for [fieldname,pretty_name],data in zip(fields, data)]
    name = data[2]

    return render_template('base_card.html', values=payload, name=name, kind='Partner',
            edit_page='/partners/edit/' + str(uid) + '/', table_page='/partners/')

@partner_blueprint.route('/partners/edit/<int:uid>/', methods=['GET', 'POST'])
@login_required
def partner_edit(uid):
    data = get_people_info(uid, 'partners')
    fields = [('type', data[1], 'Тип', True),
              ('name', data[2], 'Имя/название', True),
              ('inn', data[3], "ИНН", True),
              ('ogrn', data[4], 'ОГРН', True),
              ('legal_address', data[5], 'Юрридический адрес', True),
              ('payment_details', data[6], 'Реквизиты', False),
              ('phone', data[8], 'Телефон для связи', True),
              ('email', data[9], 'Email', True),
              ('socials', data[10], 'Социальные сети', False),
              ('website', data[11], 'Сайт', True),
              ('sphere', data[12], 'Сфера деятельности', True),
              ('category', data[13], 'Категория', True),
              ('comment', data[14], 'Комментарий', False)]

    if data is None:
        abort(404)

    return render_template('base_edit.html', values=fields, who='партнёре', 
                edit_to="/partners/edited/" + str(uid) + '/')

@partner_blueprint.route('/partners/edited/<int:uid>/', methods=['POST'])
@login_required
def parnter_edited(uid):

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
        q = 'update partners set '
        for i,j in zip(cols, vals):
            if j != '\'None\'':
                q += f'{i} = {j},'

        q += f'updated_at = now() where id = {uid}'
        with db.connect() as con:
            con.execute(q)

    return redirect('/partners/')