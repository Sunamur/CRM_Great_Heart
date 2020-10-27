# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>


from flask import Blueprint, redirect, render_template
from flask import request, url_for
from flask_user import current_user, login_required, roles_required

from app import db
from app.models.user_models import UserProfileForm, User

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# The Home page is accessible to anyone
@main_blueprint.route('/')
def home_page():
    return render_template('main/home_page.html')


# The User page is accessible to authenticated users (users that have logged in)
@main_blueprint.route('/member')
@login_required  # Limits access to authenticated users
def member_page():
    return render_template('main/user_page.html')


# The Admin page is accessible to users with the 'admin' role
@main_blueprint.route('/admin')
@roles_required('admin')  # Limits access to users with the 'admin' role
def admin_page():
    return render_template('main/admin_page.html')


@main_blueprint.route('/main/profile', methods=['GET', 'POST'])
@login_required
def user_profile_page():
    # Initialize form
    form = UserProfileForm(request.form, obj=current_user)

    # Process valid POST
    if request.method == 'POST' and form.validate():
        # Copy form fields to user_profile fields
        form.populate_obj(current_user)

        # Save user_profile
        db.session.commit()

        # Redirect to home page
        return redirect(url_for('main.home_page'))

    # Process GET or invalid POST
    return render_template('main/user_profile_page.html',
                           form=form)


@main_blueprint.route('/main/users', methods=['GET','POST'])
@login_required
def user_list():
    users = User.query.all() 
    header = ['id','first_name','last_name','username','roles']
    values=[[
        user.id,
        user.first_name,
        user.last_name,
        user.username,
        get_roles(user.roles)
    ] for user in users]
    
    return render_template('main/table_users.html',header=header, values=values)



@main_blueprint.route('/main/<int:id>/user', methods=['GET'])
@login_required
def user_card(id):
    user = User.query.filter_by(id=id).first()
    values = {
        'id':user.id,
        'first_name':user.first_name,
        'last_name':user.last_name,
        'username':user.username,
        'roles':get_roles(user.roles)

    }
    
    return render_template('main/user_card.html', values=values)

def get_roles(roles):
    try:
        return '; '.join([role for role in roles])
    except TypeError:
        'No roles'