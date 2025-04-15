from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user
from App.models import InternAdmin, Ship, Intern

from.index import index_views

from App.controllers import (
    # create_user,
    create_admin,
    authenticate, 
    get_all_users,
    get_all_users_json,
    create_intern,
    get_all_intern,
    get_intern,
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    interns = get_all_intern()
    return render_template('users.html', users=users, interns=interns)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_admin(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})


@user_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_admin(data['username'], data['password'], data['name'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/users/interns', methods=['POST'])
def create_intern_action():
    data = request.form
    exist= get_intern(data['school_id'])
    if exist:
        flash(f"Intern alread exists!")
    else:
        flash(f"Intern {data['name']} created!")
        create_intern(data['name'], data['school_id'], data['dept'], data['course'], data['year'], data['GPA'])
    return redirect(url_for('user_views.get_user_page'))

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')