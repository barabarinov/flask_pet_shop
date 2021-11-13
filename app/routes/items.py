from flask import request
from flask_api import status
from flask_api.exceptions import NotFound
from flask_login import current_user, login_required

from app import app, db
from app.models import Item


@app.route('/items/', methods=['GET', 'POST'])
@login_required
def all_items_of_current_user_handler():
    if request.method == 'GET':
        return [item.to_json() for item in current_user.items]
    else:
        user_input = request.get_json()
        item = Item(
            created_by_user_id=current_user.id,
            title=user_input['title'],
            amount=user_input['amount'],
            price=user_input['price'],
        )
        db.session.add(item)
        db.session.commit()
        return item.to_json(), status.HTTP_201_CREATED


@app.route('/items/<int:item_id>/', methods=['GET', 'PUT', 'DELETE'])
@login_required
def single_item_of_current_user_handler(item_id):
    item: Item = Item.query.get(item_id)
    if item is None or item.user != current_user:
        raise NotFound('Item not found')
    if request.method == 'GET':
        response_data = item.to_json()
    elif request.method == 'PUT':
        user_input = request.get_json()
        item.title = user_input['title']
        item.amount = user_input['amount']
        item.price = user_input['price']
        db.session.commit()
        response_data = item.to_json()
    else:
        db.session.delete(item)
        db.session.commit()
        response_data = {'message': 'Successful deleted item'}
    return response_data


@app.route('/items/all/', methods=['GET'])
@login_required
def all_items_of_all_users_handler():
    return [item.to_json() for item in db.session.query(Item).all()]


@app.route('/items/all/<int:item_id>/', methods=['GET'])
@login_required
def single_item_of_all_users_handler(item_id):
    item: Item = Item.query.get(item_id)
    if item is None:
        raise NotFound('Item not found!')
    else:
        return item.to_json()


@app.route('/items/calculate/', methods=['GET'])
@login_required
def sum_of_all_prices():
    result = 0
    for item in Item.query.filter(Item.price > 0).all():
        result += item.amount * item.price
    return {'message': f'Sum of all prices of items = {result}'}
