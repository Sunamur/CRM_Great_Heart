import os, time, datetime
from flask import Flask, flash, url_for, redirect, render_template, request, session, abort, send_from_directory, send_file, Response
from flask_sqlalchemy import SQLAlchemy as flask_sqlalchemy
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from wtforms.validators import DataRequired, URL
from wtforms import TextField, Form, SubmitField, SelectField
import json
import enum
import psycopg2

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = flask_sqlalchemy(app)

base = automap_base()

engine = db.create_engine('postgres://obcayovm:ItiplxDZiHmnUo_7WdFtv3M67FcW1sCM@hattie.db.elephantsql.com:5432/obcayovm', {})

base.prepare(engine, reflect=True)
User = base.classes.users

ses = Session(bind=engine)

say = ses.query(User).first()
print(say.email_personal)

# connection = engine.connect()
# connection.close()
# engine.dispose()

class SearchForm(Form):
    autocomp = TextField(u"Введите имя", id='city_autocomplete')
    submit = SubmitField(u'Поиск')


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.user_id'))
)

class Role(db.Model, RoleMixin):
    user_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    birth_date = db.Column(db.String(10))
    city = db.Column(db.String(20), unique=False, nullable=False, default='')
    phone_personal = db.Column(db.String(20), unique=False, nullable=False, default='')
    # email = db.Column(db.String(255), unique=True)
    email_personal = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    active = db.Column(db.Boolean())
    # roles = db.relationship('Role', secondary=roles_users,
    #                         backref=db.backref('users', lazy='dynamic'))
    

    def __str__(self):
        return self.email_personal

class slaves_state_Enum(enum.Enum):
    heavy = 'heavy'
    diseased = 'diseased'
    treatment = 'treatment'
    reabilitation = 'reabilitation'
    remission = 'remission'

class partner_type_Enum(enum.Enum):
    phys = 'natural person'
    law = 'legal entity'

class partner_category_Enum(enum.Enum):
    vip = 'vip'
    ordinary = 'ordinary'


# Определяем модель для всей таблици ############################################
class Slaves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), unique=True, nullable=False)
    birth_date = db.Column(db.Date, unique=False, nullable=False, default='')
    state = db.Column(db.Enum(slaves_state_Enum), unique=False, nullable=False, default='')
    city = db.Column(db.String(20), unique=False, nullable=False, default='')
    phone_1 = db.Column(db.String(20), unique=False, nullable=False, default='')
    phone_2 = db.Column(db.String(20), unique=False, nullable=False, default='')
    telegram = db.Column(db.String(20), unique=False, nullable=False, default='')
    email = db.Column(db.String(50), unique=False, nullable=False, default='')
    profession = db.Column(db.String(50), unique=False, nullable=False, default='')
    hobbies = db.Column(db.String(50), unique=False, nullable=False, default='')
    comment = db.Column(db.String(100), unique=False, nullable=False, default='')
    # queries = db.Column(db.String(100), unique=False, nullable=False, default='')

    def __repr__(self):
        return self.fullname

class Partners(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.Enum(partner_type_Enum), unique=False, nullable=False, default='')
    reg_requisites= db.Column(db.String(100), unique=False, nullable=False, default='')
    payment_requisites= db.Column(db.String(100), unique=False, nullable=False, default='')
    # logo = 0
    # contacts = 
    phone = db.Column(db.String(20), unique=False, nullable=False, default='')
    email = db.Column(db.String(50), unique=False, nullable=False, default='')
    socials = db.Column(db.String(50), unique=False, nullable=False, default='')
    site = db.Column(db.String(50), unique=False, nullable=False, default='')
    # partnership = 
    category = db.Column(db.Enum(partner_category_Enum), unique=False, nullable=False, default='')
    comment = db.Column(db.String(100), unique=False, nullable=False, default='')

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.Enum(partner_type_Enum), unique=False, nullable=False, default='')
    reg_requisites= db.Column(db.String(100), unique=False, nullable=False, default='')
    payment_requisites= db.Column(db.String(100), unique=False, nullable=False, default='')
    # logo = 0
    # contacts = 
    phone = db.Column(db.String(20), unique=False, nullable=False, default='')
    email = db.Column(db.String(50), unique=False, nullable=False, default='')
    socials = db.Column(db.String(50), unique=False, nullable=False, default='')
    site = db.Column(db.String(50), unique=False, nullable=False, default='')
    category = db.Column(db.Enum(partner_category_Enum), unique=False, nullable=False, default='')
    comment = db.Column(db.String(100), unique=False, nullable=False, default='')
    #payments

class Benefactor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), unique=True, nullable=False)
    birth_date = db.Column(db.Date, unique=False, nullable=False, default='')
    phone = db.Column(db.String(20), unique=False, nullable=False, default='')
    telegram = db.Column(db.String(20), unique=False, nullable=False, default='')
    email = db.Column(db.String(50), unique=False, nullable=False, default='')
    socials = db.Column(db.String(50), unique=False, nullable=False, default='')
    comment = db.Column(db.String(100), unique=False, nullable=False, default='')
    category = db.Column(db.Enum(partner_category_Enum), unique=False, nullable=False, default='')
    comment = db.Column(db.String(100), unique=False, nullable=False, default='')
    #payments
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # type = 
    # date = 
    # description = 
    # headliners =
    # place =
    # partners =
    # sponsors = 
    # planned_guests =
    # fact_guests =
    # review =


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(engine, Users, Role)
security = Security(app, user_datastore)


# Create customized model view class
class superuser_ModVw(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


##################################################################################################
################  определяем вюшки ###############################################################
##################################################################################################
class DirReg_ALL_ModVw(sqla.ModelView):

    def is_accessible(self):
        ROLLE = 'ALL'
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role(ROLLE):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

    # create_modal = True
    # edit_modal = True
    # can_export = True
    page_size = 50
    column_searchable_list = ('fullname', 'phone_1')
    column_default_sort = 'fullname'
    column_labels = dict(fullname="Имя", profession='Профессия', phone_1='Основной', phone_2='Дополнительный', city='Город')
    form_args = {
        'fullname': {'label': "Имя", 'validators': [DataRequired()]},
        'profession': {'label': 'Профессия'},
        'phone_1': {'label': "Внутренний номер телефона №1"},
        'phone_2': {'label': "Внутренний номер телефона №2"},
        'city': {'label': "Город"}
    }
    # form_choices = {
    #     'company': [
    #         ('', '-'),
    #         ('Киев', 'Киев'),
    #         ('Львов', 'Львов'),
    #         ('Лондон', 'Лондон'),
    #     ]
    # }




########################################################################################################################
######### FLASK VIEWS ##################################################################################################
########################################################################################################################

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    fullnames_raw = Slaves.query.all()
    fullnames = []
    for i in fullnames_raw:
        fullnames.append(str(i))
    return Response(json.dumps(fullnames), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect('/login')


@app.route('/select', methods=['GET', 'POST'])
def select():
    # name = request.form.get('autocomp')
    # PAO = request.form.get('PAO')
    # if name == None:
    #     return redirect('/')
    # if name == "" and PAO == "Все":
    #     return redirect('/')
    # elif name != "" and PAO != "Все":
    #     query = 'SELECT name, surname, diagnosis, position, int_1, mob_1, email, id from  where fullname like "' + name + '%" and company = "' + PAO + '" ORDER BY fullname'
    # elif name == "" and PAO != "Все":
    #     query = 'SELECT fullname, company, position,int_1, mob_1, email, id  from Slaves where company = "' + PAO + '" ORDER BY fullname'
    # elif name != "" and PAO == "Все":
    #     query = 'SELECT fullname, company, position, int_1, mob_1, email, id from Slaves where fullname like "' + name + '%" ORDER BY fullname'
    # else:
    #     return redirect('/')
    query = 'SELECT fullname, company, position from users'
    try: 
        # connection = psycopg2.connect(user = 'obcayovm',
        #                               password = 'ItiplxDZiHmnUo_7WdFtv3M67FcW1sCM',
        #                               port = '5432', 
        #                               host = 'hattie.db.elephantsql.com')
        cursor = engine.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        # connection.close()      
        form = SearchForm(request.form)
        return render_template('formselect.html', form=form, data=records)
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)


################## Detail
@app.route("/detail/<id>", methods=['GET', 'POST'])
def detail(id):
    query = 'SELECT * from clients where id = "' + id + '"'
    try:
        # connection = psycopg2.connect(user = 'obcayovm',
        #                               password = 'ItiplxDZiHmnUo_7WdFtv3M67FcW1sCM',
        #                               port = '5432', 
        #                               host = 'hattie.db.elephantsql.com')
        cursor = engine.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        # connection.close()

        laa = []
        for i in records:
            for x in i:
                laa.append(str(x))
        sname = laa[1]
        return render_template('detail.html', sname=sname, data=records)
    except Exception as e:
        return (str(e))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Create admin
admin = flask_admin.Admin(
    app,
    u'Great Heart CRM',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# model views для Администрирования
admin.add_view(superuser_ModVw(Role, db.session))
admin.add_view(superuser_ModVw(Users, db.session))
# model view для Всей таблици
admin.add_view(DirReg_ALL_ModVw(Slaves, db.session))

@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )




if __name__ == "__main__":
    app.secret_key = os.urandom(100)
    app.run(debug=True,host='127.0.0.1', port=5000)