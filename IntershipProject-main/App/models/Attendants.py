from App.database import db
from App.models import Ship, Intern
from flask import Flask



class Attendants(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)
    intern_id = db.Column(db.Integer, db.ForeignKey('intern.school_id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)

#   intern = db.relationship('intern', backref=db.backref('attendees', lazy='joined'))
 
    def __init__(self, id, ship_id, intern_id,name):
        self.ship_id = ship_id
        self.intern_id = intern_id
        self.id = id
        self.name= name
    


    def get_json(self):
        return {
        "Internship ID": self.ship.id,
        "Intern ID": self.intern.id,
        # "Internship Name": self.ship_id.name,
        "Intern Name": self.name
        }
    pass
