from multiprocessing.sharedctypes import Value
from tkinter.tix import INTEGER
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    phone_number = db.Column(db.String(10))
    type = db.Column(db.String(1))
    account_number = db.Column(db.String(10))
    balance = db.Column(db.Integer)
    conductors = db.relationship('Conductor_details')
    scratch_cards = db.relationship('Scratch_card')
    helpdesk_recharges = db.relationship('Helpdesk_recharge')

class Conductor_details(db.Model, UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    conductor_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    bus = db.Column(db.String(10))

class Route(db.Model):
    route_id = db.Column(db.Text , primary_key = True)
    start =db.Column(db.String(100))
    end =db.Column(db.String(100))
    stops = db.Column(db.String(100))

class Scratch_card(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    card_number =db.Column(db.Integer)
    security_hash = db.Column(db.Integer)
    value = db.Column(db.Integer)
    status = db.Column(db.String(1))
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))
    date = db.Column(db.String(10))
    
class Site_settings(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    scratch_card_run = db.Column(db.Integer)

class Helpdesk_recharge(db.Model,UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    value = db.Column(db.Integer)
    date = db.Column(db.String(100))
    account_number = db.Column(db.String(10) , db.ForeignKey('user.account_number'))