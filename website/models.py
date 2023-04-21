from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class CandleData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    close = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    information = db.Column(db.String(150))
    timestamp = db.Column(db.Integer)

class BacktestTransactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    information = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    method_preference = db.Column(db.Integer)
    manual_automatic_preference = db.Column(db.Integer)
    api_key = db.Column(db.String(150))
    api_secret = db.Column(db.String(150))