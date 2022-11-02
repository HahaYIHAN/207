from unicodedata import category
from . import db
from datetime import date, datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'  # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, index=True, nullable=False)
    address = db.Column(db.String(100), index=True, nullable=False)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    # password is never stored in the DB, an encrypted password is stored
    # the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    category = db.Column(db.String(255))
    price = db.Column(db.String(3))
    tickets = db.Column(db.Integer)
    status = db.Column(db.String(100))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    website = db.Column(db.String(255))
    address = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.now)
    # ... Create the Comments db.relationship
    # relation to call event.comments and comment.event
    user = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event')

    def __repr__(self):  # string print method
        return "<Name: {}>".format(self.name)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    def __repr__(self):  # string print method
        return "<Order: {}>".format(self.count)
 

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now)
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)

