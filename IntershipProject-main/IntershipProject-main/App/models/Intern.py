from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class Intern(db.Model):
    # id = db.Column(db.Integer, primary_key=True, unique=True)
    school_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    dept = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(120), nullable=True)
    year = db.Column(db.Integer, nullable=False)
    GPA = db.Column(db.Integer, nullable=False)
    
    def __init__(self, name, school_id, dept, course, year, GPA):
        self.name= name
        self.school_id= school_id
        self.dept= dept
        self.course= course
        self.year= year
        self.GPA= GPA

    def get_json(self):
        return{
            'ID': self.school_id,
            'Name': self.name,
            'Department': self.dept,
            'GPA': self.GPA
        }

    def add_course(self, course):
        self.courses.append(course + " ")
        db.session.add(self)
        db.session.commit()

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)
            db.session.add(self)
            db.session.commit()

