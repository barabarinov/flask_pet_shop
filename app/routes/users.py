from flask_login import current_user, login_required

from app import app, db
from app.models import User


@app.route('/user-info/', methods=['GET'])
@login_required
def user_info():
    return current_user.to_json()


@app.route('/users/', methods=['GET'])
@login_required
def get_users():
    return [user.to_json() for user in db.session.query(User).all()]
