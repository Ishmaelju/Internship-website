import os
from flask import Flask, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta


from App.database import init_db, db

from App.controllers import (
    setup_jwt
)
from App.models import (
    User,
    InternAdmin,
    Ship,
    Intern,
)

# from App.views import (
#     home_views,
#     index_views,
#     login_views,
#     signup_views,
#     user_views,
# )

from App.views import views


def add_views(app):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    delta = 7
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
        delta = app.config['JWT_ACCESS_TOKEN_EXPIRES']
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        delta = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 7)
        
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(delta))
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
        
    for key, value in config.items():
        app.config[key] = config[key]



login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash(f'Unauthorized!')
    return redirect('/login')

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEVER_NAME'] = '0.0.0.0'
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app)
    init_db(app)
    setup_jwt(app)
    login_manager.init_app(app)
    login_manager.login_view = "login_page"
    # added this cause the wsgi wasnt making the database
    with app.app_context():
        db.create_all()
    app.app_context().push()
    return app