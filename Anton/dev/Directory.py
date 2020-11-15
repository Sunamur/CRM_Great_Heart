#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
import os, time, datetime
from flask import Flask, flash, url_for, redirect, render_template, request, session, abort, send_from_directory, send_file, Response
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from wtforms.validators import DataRequired
from wtforms import TextField, Form, SubmitField, SelectField
import json
from sqlalchemy.orm import sessionmaker
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')




# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

class SearchForm(Form):
    autocomp = TextField(u"Введите имя", id='city_autocomplete')
    submit = SubmitField(u'Поиск')


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

# Определяем модель для всей таблици ############################################
class directory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), unique=True, nullable=False)
    position = db.Column(db.String(200), unique=False, nullable=False, default='')
    company = db.Column(db.String(30), unique=False, nullable=False, default='')
    int_1 = db.Column(db.String(20), unique=False, nullable=False, default='')
    int_2 = db.Column(db.String(20), unique=False, nullable=False, default='')
    int_3 = db.Column(db.String(20), unique=False, nullable=False, default='')
    srv_1 = db.Column(db.String(20), unique=False, nullable=False, default='')
    srv_2 = db.Column(db.String(20), unique=False, nullable=False, default='')
    srv_3 = db.Column(db.String(20), unique=False, nullable=False, default='')
    mob_1 = db.Column(db.String(20), unique=False, nullable=False, default='')
    mob_2 = db.Column(db.String(20), unique=False, nullable=False, default='')
    mob_3 = db.Column(db.String(20), unique=False, nullable=False, default='')
    viber = db.Column(db.String(20), unique=False, nullable=False, default='')
    telegram = db.Column(db.String(20), unique=False, nullable=False, default='')
    whatsup = db.Column(db.String(20), unique=False, nullable=False, default='')
    city = db.Column(db.String(20), unique=False, nullable=False, default='')
    srv_1 = db.Column(db.String(20), unique=False, nullable=False, default='')
    srv_2 = db.Column(db.String(20), unique=False, nullable=False, default='')
    srv_3 = db.Column(db.String(20), unique=False, nullable=False, default='')
    email = db.Column(db.String(50), unique=False, nullable=False, default='')
    home = db.Column(db.String(20), unique=False, nullable=False, default='')
    fax = db.Column(db.String(20), unique=False, nullable=False, default='')
    skype = db.Column(db.String(20), unique=False, nullable=False, default='')

    def __repr__(self):
        return self.fullname

# Наследуем модель Directory и переопределяем repr ############################################
class FnNum(directory):
    def __repr__(self):
        return self.int_1 + " : " + self.fullname


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
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


    column_exclude_list = ['position', 'int_2', 'int_3', 'mob_2', 'mob_3', 'viber', 'telegram', 'whatsup', 'srv_2', 'srv_3',
                           'home', 'fax', 'skype']
    # create_modal = True
    # edit_modal = True
    # can_export = True
    page_size = 50
    column_searchable_list = ('fullname', 'int_1')
    column_default_sort = 'fullname'
    column_labels = dict(fullname="Имя", company='Подразделение', int_1='Внутр.', mob_1='Моб.', city='Городской',
                         srv_1='Сервисный')
    form_args = {
        'fullname': {'label': "Имя", 'validators': [DataRequired()]},
        'position': {'label': 'Должность'},
        'company': {'label': 'Подразделение'},
        'int_1': {'label': "Внутренний номер телефона №1"},
        'int_2': {'label': "Внутренний номер телефона №2"},
        'int_3': {'label': "Внутренний номер телефона №3"},
        'mob_1': {'label': "Мобильный номер телефона №1"},
        'mob_2': {'label': "Мобильный номер телефона №2"},
        'mob_3': {'label': "Мобильный номер телефона №3"},
        'city': {'label': "Городской номер телефона"},
        'srv_1': {'label': "Сервисный номер телефона №1"},
        'srv_2': {'label': "Сервисный номер телефона №2"},
        'srv_3': {'label': "Сервисный номер телефона №3"},
        'home': {'label': "Домашний номер телефона"}
    }
    form_choices = {
        'company': [
            ('', '-'),
            ('Киев', 'Киев'),
            ('Львов', 'Львов'),
            ('Лондон', 'Лондон'),
        ]
    }




########################################################################################################################
######### FLASK VIEWS ##################################################################################################
########################################################################################################################

@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    fullnames_raw = directory.query.all()
    fullnames = []
    for i in fullnames_raw:
        fullnames.append(str(i))
    return Response(json.dumps(fullnames), mimetype='application/json')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = SearchForm(request.form)
    return render_template('index.html', form=form)


@app.route('/select', methods=['GET', 'POST'])
def select():
    name = request.form.get('autocomp')
    PAO = request.form.get('PAO')
    if name == None:
        return redirect('/')
    if name == "" and PAO == "Все":
        return redirect('/')
    elif name != "" and PAO != "Все":
        query = 'SELECT fullname, company, position, int_1, mob_1, email, id from directory where fullname like "' + name + '%" and company = "' + PAO + '" ORDER BY fullname'
    elif name == "" and PAO != "Все":
        query = 'SELECT fullname, company, position,int_1, mob_1, email, id  from directory where company = "' + PAO + '" ORDER BY fullname'
    elif name != "" and PAO == "Все":
        query = 'SELECT fullname, company, position, int_1, mob_1, email, id from directory where fullname like "' + name + '%" ORDER BY fullname'
    else:
        return redirect('/')
    # return query
    try:
        con = sqlite3.connect('Directory.db')
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        con.close()
        form = SearchForm(request.form)
        return render_template('formselect.html', form=form, data=data)
    except Exception as e:
        return (str(e))


################## Detail
@app.route("/detail/<id>", methods=['GET', 'POST'])
def detail(id):
    query = 'SELECT * from directory where id = "' + id + '"'
    try:
        con = sqlite3.connect('Directory.db')
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        con.close()

        laa = []
        for i in data:
            for x in i:
                laa.append(str(x))
        sname = laa[1]
        return render_template('detail.html', sname=sname, data=data)
    except Exception as e:
        return (str(e))

@app.route("/services", methods=['GET'])
def services():
    srv_5000 = FnNum.query.filter((FnNum.srv_1 == "5000") | (FnNum.srv_2 == "5000") | (FnNum.srv_3 == "5000")).all()
    srv_5001 = FnNum.query.filter((FnNum.srv_1 == "5001") | (FnNum.srv_2 == "5001") | (FnNum.srv_3 == "5001")).all()
    return render_template('services.html', srv_5000=srv_5000, srv_5001=srv_5001)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Create admin
admin = flask_admin.Admin(
    app,
    u'Телефонный справочник',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# model views для Администрирования
admin.add_view(superuser_ModVw(Role, db.session))
admin.add_view(superuser_ModVw(User, db.session))
# model view для Всей таблици
admin.add_view(DirReg_ALL_ModVw(directory, db.session))

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
    app.run(debug=True,host='0.0.0.0', port=5000)
