import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

from App.main import create_app
from App.database import create_db
from App.models import Ship
from App.controllers import (
    create_ship,
    get_ship,
    get_all_ship_json,
    get_ship_by_name,
    update_ship_name,
    update_desc,
    update_location,
    update_datetime,
    update_spots,
    del_ship,
)

from wsgi import app
db.drop_all()
db.create_all()


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class InternshipUnitTests(unittest.TestCase):

    def test_new_ship(self):
        ship = Ship("first ship", "its first", "UWI","2022,10,5, 9:30", 30)
        assert ship.name == "first ship"

    # pure function no side effects or integrations called
    def test_get_json(self):
        ship = Ship("first ship", "its first", "UWI","2022,10,5, 9:30", 30)
        ship_json = ship.get_json()
        self.assertDictEqual(ship_json, {"name":"first ship", "description":"its first", "location":"UWI", "Date and Time": "2022,10,5, 9:30", "Spots Remaining": 30, "Enrolled": 0})
    

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app.config.update({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    # workaround for error
    if app== None:
        create_db(app)
    yield app.test_client()
    os.unlink(os.getcwd()+'/App/test.db')
    db.drop_all()


class InternshipIntegrationTests(unittest.TestCase):

    def test_1create_ship(self):
        ship = create_ship("first ship", "its first", "UWI","2022,10,5, 9:30", 30)
        assert ship.name == "first ship"

    def test_2get_all_ship_json(self):
        ship_json = get_all_ship_json()
        self.assertListEqual([{"name":"first ship", "description":"its first", "location":"UWI", "Date and Time":"2022,10,5, 9:30","Spots Remaining":30, "Enrolled":0}], ship_json)
    
    def test_rename_ship(self):
        ship = update_ship_name(1,'tester')
        assert ship.name == "tester"

    def test_change_description(self):
        ship = update_desc(1,'changed')
        assert ship.desc == "changed"

    # def test_change_location(self):
    #     ship = update_location(1,'earth')
    #     assert ship.location == "earth"

    # def test_change_datetime(self):
    #     ship = update_datetime(1,'2022-2-2 6pm')
    #     assert ship.date_time == "2022-2-2 6pm"

    # def test_change_spots(self):
    #     ship = update_spots(1,50)
    #     assert ship.spots == 50

    # def test_delete_ship(self):
    #     ship = del_ship(1)
    #     assert ship == None
        

