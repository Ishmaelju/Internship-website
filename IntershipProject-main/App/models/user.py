from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=True)

    def __init__(self, username, password, name):
        self.username = username
        self.set_password(password)
        self.name = name

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'name': self.name
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

