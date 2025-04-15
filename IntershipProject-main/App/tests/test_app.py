import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

from App.main import create_app
from App.database import create_db
from App.models import User, InternAdmin, Ship
from App.controllers import (
    create_user,
    get_all_users_json,
    authenticate,
    get_user,
    get_user_by_username,
    update_user,
    
    create_admin,
    authenticate,
    get_all_admin_json,
    get_admin,
    get_admin_by_username,
    get_admin_by_name,
    update_admin,
    
    create_ship,
    get_ship,
    get_all_ship_json,
    get_ship_by_name
)

from wsgi import app
db.drop_all()
db.create_all()

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass", "bobby")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass", "bobby")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "name":"bobby"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password, 'bobby')
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password, 'bobby')
        assert user.check_password(password)

# class InternAdminUnitTests(unittest.TestCase):

#     def test_new_admin(self):
#         admin = InternAdmin("bob", "bobpass", "bobby")
#         assert admin.username == "bob"

#     # pure function no side effects or integrations called
#     def test_get_json(self):
#         admin = InternAdmin("bob", "bobpass", "bobby")
#         admin_json = admin.get_json()
#         self.assertDictEqual(admin_json, {"id":None, "username":"bob", "name":"bobby"})
    
#     def test_hashed_password(self):
#         password = "mypass"
#         hashed = generate_password_hash(password, method='sha256')
#         admin = InternAdmin("bob", password,'bobby')
#         assert admin.password != password

#     def test_check_password(self):
#         password = "mypass"
#         admin = InternAdmin("bob", password, 'bobby')
#         assert admin.check_password(password)

# class InternshipUnitTests(unittest.TestCase):

#     def test_new_ship(self):
#         ship = Ship("first ship", "its first", "UWI","2022,10,5, 9:30", 30)
#         assert ship.name == "first ship"

#     # pure function no side effects or integrations called
#     def test_get_json(self):
#         ship = Ship("first ship", "its first", "UWI","2022,10,5, 9:30", 30)
#         ship_json = ship.get_json()
#         self.assertDictEqual(ship_json, {"id":None, "name":"first ship"})
    


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


class UsersIntegrationTests(unittest.TestCase):

    def test_authenticate(self):
        user = create_user("bob", "bobpass", "bobby")
        assert authenticate("bob", "bobpass") != None

    def test_1create_user(self):
        user = create_user("rickster", "bobpass", "rick")
        assert user.username == "rickster"

    # def test_2get_all_users_json(self):
    #     users_json = get_all_users_json()
    #     self.assertListEqual([{"id":1, "username":"bob", "name":"bobby"}, {"id":2, "username":"rickster", "name":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"
