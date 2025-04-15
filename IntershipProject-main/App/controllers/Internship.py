from App.models import Internship
from App.database import db
from datetime import datetime
from flask import flash

#Internship Controllers
# --------------------------------------------------------------------------------
def create_internship(name, desc, location, date_time, openspots):
    internship = Internship(name=name, desc=desc, location=location, date_time = date_time, openspots = openspots)
    if internship:
        db.session.add(internship)
        db.session.commit()
        return internship
    return None
    # datetime(year, month, day, hour, minute, second, microsecond)
    # b = datetime(2022, 12, 28, 23, 55, 59, 342380)
    
def get_internship(id):
    return Internship.query.get(id)

def get_all_internship():
    return Internship.query.all()

def get_all_internship_json():
    internships = Internship.query.all()
    if not internships:
        return []
    internships = [internship.get_json() for internship in internships]
    return internships

def update_internship_name(id, name):
    internship = get_internship(id)
    if internship:
        internship.name = name
        db.session.add(internship)
        return db.session.commit()
    return None

    
# Update Controllers
# --------------------------------------------------------------------------------------
#Name 
def update_name(id, name):
    internship = get_internship(id)
    if internship:
        internship.name = name
        db.session.add(internship)
        return db.session.commit()
    return None

#Description 
def update_desc(id, desc):
    internship = get_internship(id)
    if internship:
        internship.des = desc
        db.session.add(internship)
        return db.session.commit()
    return None
    
# Location
def update_location(id, loc):
    internship = get_internship(id)
    if internship:
        internship.location = loc
        db.session.add(internship)
        return db.session.commit()
    return None  

# Open Spots
def update_spots(id, spots):
    internship = get_internship(id)
    if internship:
        internship.openspots = spots
        db.session.add(internship)
        return db.session.commit()
    return None  

# Enrolled
def update_enrolled(id, er):
    internship = get_internship(id)
    if internship:
        internship.enrolled = er
        db.session.add(internship)
        return db.session.commit()
    return None

def update_datetime(id, date_time):
    internship = get_internship(id)
    if internship:
        try:
            # Parse the date string to a datetime object
            date_time_obj = datetime.datetime.strptime(date_time, "%Y/%m/%d")
            # Format the datetime object back to a string in the desired format
            formatted_date_time = date_time_obj.strftime("%Y/%m/%d")
            ship.date_time = formatted_date_time
            db.session.add(internship)
            db.session.commit()
            return ship
        except ValueError:
            # Handle invalid date format error
            flash(f"Invalid date format. Please use the format 'year/month/day'.  ")
            return None
    return None
