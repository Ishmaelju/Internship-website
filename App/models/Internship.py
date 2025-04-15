from App.database import db
from flask_login import UserMixin
from datetime import datetime

class Internship(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(120), nullable=False, unique=False)
    desc =  db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=False)
    date_time = db.Column(db.Date, nullable=False)
    openspots = db.Column(db.Integer, nullable=False)
    enrolled = db.Column(db.Integer, nullable=True)


    def __init__(self, name, desc, location, date_time, openspots):
        self.name = name
        self.desc= desc
        self.location = location
        self.date_time = date_time
        self.openspots = openspots
        self.enrolled = 0


    def get_json(self):
        return{
            'Name': self.name,
            'Description': self.desc,
            'Location': self.location,
            'Date and Time': self.date_time,
            'Spots Remainng': self.openspots,
            'Enrolled': self.enrolled
        }
