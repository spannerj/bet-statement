from odds_monkey.extensions import db
from sqlalchemy.dialects.postgresql import JSON
from flask_login import UserMixin
from odds_monkey.app import login


class Statement(db.Model):
    __tablename__ = 'statement'

    id = db.Column(db.Integer, primary_key=True)
    statement = db.Column(JSON)


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    players = db.Column(JSON)


class User(UserMixin, db.Model):
    """"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    page_route = db.Column(db.String)
    full_name = db.Column(db.String)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Payment(UserMixin, db.Model):
    """"""
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String)
    amount = db.Column(db.Integer)
    payment_date = db.Column(db.Date)
