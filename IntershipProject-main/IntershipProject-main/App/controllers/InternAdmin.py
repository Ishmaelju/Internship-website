from App.models import InternAdmin, Internship, Ship
from App.database import db

# testing
def make_ship(name, desc, location, date_time, openspots):
    ship= create_ship(name, desc, location, date_time, openspots)
    return ship


#InternAdmin Controllers
# --------------------------------------------------------------------------------
def create_admin(username, password, name):
    exists = get_admin_by_username(username)
    if exists:
        flash(f'User already exists!')
        return None
    admin = InternAdmin(username=username, password=password, name=name)
    if admin:
        admin.username = username
        db.session.add(admin)
        db.session.commit()
        return admin
    return None

def get_admin_by_username(username):
    return InternAdmin.query.filter_by(username=username).first()

def get_admin_by_name(name):
    return InternAdmin.query.filter_by(name=name).first()

def get_admin(id):
    return InternAdmin.query.get(id)

def get_all_admin():
    return InternAdmin.query.all()

def get_all_admin_json():
    admins = InternAdmin.query.all()
    if not admins:
        return []
    admins = [admin.get_json() for admin in admins]
    return admins

def update_admin(id, username):
    admin = get_admin(id)
    if admin:
        admin.username = username
        db.session.add(admin)
        return db.session.commit()
    return None

#Internship Controllers
# --------------------------------------------------------------------------------
    
def change_name(id, name):
    internship = get_internship(id)
    if internship:
        internship = update_name(id,name)
        return internship
    return None   

def change_desc(id, desc):
    internship = get_internship(id)
    if internship:
        internship = update_desc(id,desc)
        return internship
    return None   

def change_location(id, loc):
    internship = get_internship(id)
    if internship:
        internship = update_location(id,loc)
        return internship
    return None
  
def change_spots(id, spots):
    internship = get_internship(id)
    if internship:
        internship = update_spots(id, spots)
        return internship
    return None
  
def change_enrolled(id, er):
    internship = get_internship(id)
    if internship:
        internship = update_enrolled(id,loc)
        return internship
    return None
  
