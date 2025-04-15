from App.database import db

class Ship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    desc = db.Column(db.String(120), nullable=True)
    location = db.Column(db.String(120), nullable=False)
    date_time = db.Column(db.String(120), nullable=False)
    openspots = db.Column(db.Integer, nullable=False)
    enrolled = db.Column(db.Integer, nullable=False)

    def __init__(self, name, desc, location, date_time, openspots):
        self.name = name
        self.desc= desc
        self.location= location
        self.date_time = date_time
        self.openspots = openspots
        self.enrolled = 0


    def get_json(self):
        return{
            'name': self.name,
            'description': self.desc,
            'location': self.location,
            'Date and Time': self.date_time,
            'Spots Remaining': self.openspots,
            'Enrolled': self.enrolled
        }
        

