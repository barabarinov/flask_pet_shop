from functools import wraps

from flask_login import current_user
from flask_api.exceptions import NotFound

from app.models import Item


def find_item_id(func):
    @wraps(func)
    def wrapper(item_id):
        item: Item = Item.query.get(item_id)
        if item is None or item.user != current_user:
            raise NotFound('Item not found')
        return func(item)
    return wrapper
