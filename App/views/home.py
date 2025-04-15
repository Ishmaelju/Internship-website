from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from App.models import InternAdmin, Intern, Ship, Attendants
from datetime import datetime

from.index import index_views

from App.controllers import (
    get_admin, 

    get_intern,
    get_all_intern,
    get_all_intern_for_ship,

    get_ship,
    get_all_ship,
    get_all_ship_json,
    create_ship,
    update_ship_name,
    update_desc,
    update_location,
    update_datetime,
    update_spots,
    update_enrolled,
    del_ship,

    get_attendee,
    add_intern_to_ship,
    del_attendee,
)

home_views = Blueprint('home_views', __name__, template_folder='../templates')


# Home Page - Working
#----------------------------------------------------------------------------
@home_views.route('/home', methods=['GET'])
@login_required
# @jwt_required()
def homepage():
    # person= get_jwt_identity()
    chosen= -1
    ships = get_all_ship()
    interns = get_all_intern()
    id = current_user.get_id()#get current user id
    admin = get_admin(id)#get the admin object
    name = admin.name #get admin name
    return render_template('home.html', admin = name, scrollers= ships, chosen=chosen, interns=interns)

# Scroll Bar Setup - Working
# ----------------------------------------------------------------------------------
@home_views.route('/home/<int:ship_id>', methods=['GET'])
@login_required
def homepage_withships(ship_id):
    chosen= get_ship(ship_id)
    if chosen== None:
        chosen=-1
    ships = get_all_ship()
    attendees = get_all_intern_for_ship(ship_id)
    interns = get_all_intern()
    if attendees == None:
        attendees= -1
    id = current_user.get_id()#get current user id
    admin = get_admin(id)#get the admin object
    name = admin.name #get admin name
    return render_template('home.html', admin = name, scrollers= ships, chosen=chosen, attendees= attendees, interns=interns)
    
# Create Internship - Working
# ----------------------------------------------------------------------------------
@home_views.route('/home', methods=['POST'])
@login_required
def make_internship():
    data = request.form
    ship  = create_ship(data['name'], data['desc'], data['location'],data['date_time'], data['openspots'] )
    # internship  = create_internship(data['name'], data['desc'], data['location'], data['openspots'], data['date_time'])
    # internship  = Internship(data['name'], data['desc'], data['location'], data['openspots'], data['date_time'])
    if ship!= None:
        flash(f"Internship {data['name']} created!")
    else:
        flash(f"Internship not created!")
    return redirect('/home/'+ str(ship.id))



# UPDATE INTERNSHIP ROUTES
# Update Internship Name - Working
# ----------------------------------------------------------------------------------
@home_views.route('/update_name/<int:ship_id>', methods=['POST'])
@login_required
def name_change(ship_id):
    ship= get_ship(ship_id)
    data = request.form
    ship = update_ship_name(ship_id,data['name'])
    if ship:
        flash(f"Internship {data['name']} changed!")
        return redirect('/home/'+ str(ship.id)) 
    else:
        flash(f"Name not changed!")
        return redirect('/home')   

# Update Internship Description - Working
# ----------------------------------------------------------------------------------
@home_views.route('/update_desc/<int:ship_id>', methods=['POST'])
@login_required
def desc_change(ship_id):
    ship= get_ship(ship_id)
    data = request.form
    ship = update_desc(ship_id,data['desc'])
    if ship:
        flash(f"Internship Description changed!")
        return redirect('/home/'+ str(ship.id)) 
    else:
        flash(f"Description not changed!")
        return redirect('/home')

# Update Internship Location - Working
# ----------------------------------------------------------------------------------
@home_views.route('/update_location/<int:ship_id>', methods=['POST'])
@login_required
def location_change(ship_id):
    ship= get_ship(ship_id)
    data = request.form
    ship = update_location(ship_id,data['location'])
    if ship:
        flash(f"Internship Location changed!")
        return redirect('/home/'+ str(ship.id)) 
    else:
        flash(f"Location not changed!")
    return redirect('/home')


# Update Internship Date and Time - NOT WORKING
# ----------------------------------------------------------------------------------
@home_views.route('/update_datetime/<int:ship_id>', methods=['POST'])
@login_required
def datetime_change(ship_id):
    ship= get_ship(ship_id)
    data = request.form
    ship = update_datetime(ship_id, data['dtime'])
    if ship:
        flash(f"Date and Time changed!")
        return redirect('/home/'+ str(ship.id)) 
    else:
        flash(f"Date and Time not changed!")
    return redirect('/home')

# Update Internship Availability - Working
# ----------------------------------------------------------------------------------
@home_views.route('/update_openspots/<int:ship_id>', methods=['POST'])
@login_required
def openspots_change(ship_id):
    ship= get_ship(ship_id)
    data = request.form
    ship = update_spots(ship_id,data['openspots'])
    if ship:
        flash(f"Internship Availability changed!")
        return redirect('/home/'+ str(ship.id)) 
    else:
        flash(f"Internship Availability not changed!")
    return redirect('/home/')


# Delete Internship - Working
# ----------------------------------------------------------------------------------
@home_views.route('/del_internship/<int:ship_id>', methods=['POST'])
@login_required
def del_internship(ship_id):
    ship= get_ship(ship_id)
    name= ship.name
    data = request.form
    ship = del_ship(ship_id)
    if ship:
        flash(name+ f" has been deleted!")
        return redirect('/home')
    else:
        flash(f"Internship could not be deleted!")
        return redirect('/home/'+ str(ship.id)) 


# Add Intern to Internship - Working
# ----------------------------------------------------------------------------------
@home_views.route('/add_intern/<int:ship_id>', methods=['POST'])
@login_required
def admit_intern(ship_id):
    data = request.form
    if ship_id is None:
        flash("Could not locate internship!")
        return redirect('/home') 
    intern = get_intern(data['id'])
    ship = get_ship(ship_id) 
    if ship.enrolled == ship.openspots:
        flash(ship.name+ f" is full!")
        return redirect('/home/'+ str(ship_id)) 

    if ship_id and intern:
        # Check if the combination already exists
        existing_attendant = Attendants.query.filter_by(ship_id=ship_id, intern_id=intern.school_id).first()
        if existing_attendant:
            flash(f"{intern.name} is already added to this internship!")
            return redirect('/home/' + str(ship_id)) 
        # Proceed with insertion

        attendee = add_intern_to_ship(ship_id, intern.school_id, intern.name)
        update = ship.enrolled + 1;
        ship = update_enrolled(ship_id, update)
        flash(intern.name+ f" has been added to "+ ship.name +"!")
        return redirect('/home/'+ str(ship_id)) 

    else:
        flash("Could not add intern to internship!")
        return redirect('/home/' + str(ship_id))


# Delete Intern from Internship - Working
# ----------------------------------------------------------------------------------
@home_views.route('/remove_intern/<int:ship_id>/<int:intern_id>', methods=['POST'])
@login_required
def delete_attendee(ship_id,intern_id):
    ship= get_ship(ship_id)
    person= get_intern(intern_id)
    id =int(str(ship_id)+str(intern_id))
    attendee = del_attendee(id)
    if attendee:
        update = ship.enrolled - 1;
        ship = update_enrolled(ship_id, update)
        flash(person.name+ f" has been deleted from "+ ship.name +"!")
        return redirect('/home/'+ str(ship.id)) 
    else:
        flash(f"Internship could not be deleted!")
        return redirect('/home/'+ str(ship.id)) 
    
# Logout - Working
# --------------------------------------------------------------------------
@home_views.route("/home/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash('Logged Out')
    return redirect('/')

