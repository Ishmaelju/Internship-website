from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db
from App.controllers import create_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass', 'bob')
    create_ship('First Internship', '', 'UWI', '2023.6/10 8am',30)
    create_intern('Patrick Star', 816000111, 'DCIT', 'COMP1602, COMP1603', 3, 3.3)
    create_intern('Betty Boop', 816000222, 'DCIT', 'COMP2602, COMP2603', 3, 3.7)
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})