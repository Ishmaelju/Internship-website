from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user,verify_jwt_in_request
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from App.models import InternAdmin, User


from.index import index_views
from App.controllers import (
    create_user,
    authenticate, 
    get_all_users,
    get_all_users_json,
)

login_views = Blueprint('login_views', __name__, template_folder='../templates')
token = ''

@login_views.route('/login', methods=['GET'])
def login():
    user= current_user.get_id()
    if user:
        flash(f'User is already logged in!')
        return redirect(url_for('home_views.homepage'))
    return render_template('login.html')

@login_views.route("/login", methods=['POST'])
def loginaction():
    data = request.form #get user data
    admin= InternAdmin.query.filter_by(username= data['username']).first()#get user account
    if admin:
        if admin.check_password(password=data['password']):
            token = authenticate(data['username'], data['password'])
            session["access_token"] = token
            # headers = {'Authorization': 'Bearer ' + token}
            login_user(admin)
            flash ('Logged in Successfully.')
            # return redirect('/home')
            return redirect(url_for('home_views.homepage'))
        else:
            flash ('Incorrect Password.')
    else:    
        flash ('Bad Username or Username Not Found.')
    return redirect('/login')
