from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # amount_of_created_items = db.Colunm(db.)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer(), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    items = db.relationship(
        'Item', back_populates='user',
        cascade='all, delete',
        passive_deletes=True,
    )

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, User):
            return self.get_id() == other.get_id()
        return NotImplemented

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
        }

    def __repr__(self):
        return f'User #{self.id}: {self.first_name} {self.last_name}'


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(30), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    user = db.relationship('User', back_populates='items')

    def to_json(self):
        return {
            'id': self.id,
            'created_by_user_id': self.created_by_user_id,
            'title': self.title,
            'amount': self.amount,
            'price': self.price,
        }

    def __repr__(self):
        return f'Item in PetShop #{self.id}: {self.title} {self.price}'
