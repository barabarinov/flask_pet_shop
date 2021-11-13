from flask_api import FlaskAPI
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = FlaskAPI(__name__)
app.secret_key = 'some secret key'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    from app.models import User

    return User.query.get(int(user_id))


from app.routes import *
from app.models import *

# import ipdb; ipdb.set_trace()
# db.drop_all()
# db.create_all()
