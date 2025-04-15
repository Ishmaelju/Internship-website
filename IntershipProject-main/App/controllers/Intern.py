from App.models import Intern, Attendants
from App.database import db

def get_intern(id):
    return Intern.query.get(id)

def get_all_intern():
    return Intern.query.all()

def get_all_intern_for_ship(id):
    return Attendants.query.filter_by(ship_id=id)

def get_all_intern_json():
    intern = Intern.query.all()
    if not intern:
        return []
    intern= [intern.get_json() for intern in intern]
    return intern

def update_intern(id, username):
    intern = get_intern(id)
    if intern:
        intern.username = username
        db.session.add(intern)
        return db.session.commit()
    return None

def create_intern(name, school_id, dept, course, year, GPA):
    intern = Intern(name=name, school_id=school_id, dept=dept, course=course, year=year, GPA=GPA)
    db.session.add(intern)
    db.session.commit()
    return intern


def update_intern(self, id, username):
    intern = self.get_intern(id)
    if intern:
        intern.username = username
        db.session.add(intern)
        db.session.commit()
        return True
    return False



def delete_intern(self, id):
        intern = self.get_intern(id)
        if intern:
            db.session.delete(intern)
            db.session.commit()
            return True
        return False




