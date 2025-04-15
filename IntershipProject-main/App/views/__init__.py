# blue prints are imported 
# explicitly instead of using *
from .home import home_views
from .login import login_views
from .index import index_views
from .signup import signup_views
from .user import user_views


views = [home_views, login_views, index_views, signup_views, user_views] 
# blueprints must be added to this list