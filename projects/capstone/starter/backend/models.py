import os, sys
from flask import Flask
from sqlalchemy import Column, String, Integer, Float
from flask_sqlalchemy import SQLAlchemy

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    print("Hello")

members = db.Table('members',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True),
    db.Column('user_id', db.Integer,db.ForeignKey('users.id'), primary_key=True)
    )    

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    outstanding = db.Column(db.Float)
    transactions = db.relationship('Transaction', backref='user_transaction', lazy=True)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    users = db.relationship('User', secondary=members, lazy='subquery',
        backref=db.backref('groups', lazy=True))
    transactions = db.relationship('Transaction', backref='group_transaction', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(120))
    date = db.Column(db.DateTime(), nullable=True)
    price = db.Column(db.Float)
    bought_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bought_for_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    bought_for_group = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)


