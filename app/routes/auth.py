from flask import request
from flask_api import status
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from app import app, db
from app.models import User


@app.route('/register/', methods=['POST'])
def register():
    request_data = request.get_json()
    new_user = User(
        username=request_data['username'],
        password=generate_password_hash(request_data['password']),
        first_name=request_data['first_name'],
        last_name=request_data['last_name'],
        age=request_data['age'],
    )
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return new_user.to_json(), status.HTTP_201_CREATED


@app.route('/login/', methods=['POST'])
def login():
    info = request.get_json()
    username, password = info['username'], info['password']
    user = db.session.query(User).filter_by(username=username).first()
    if user is not None:
        if check_password_hash(user.password, password):
            login_user(user)
            return user.to_json()
    return {"reason": "Username or password are incorrect"}, status.HTTP_401_UNAUTHORIZED


@app.route('/logout/', methods=['POST'])
def logout():
    logout_user()
    return {'message': 'Logout was successful'}
