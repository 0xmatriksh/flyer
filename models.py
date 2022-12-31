"""Models.py"""
from app import db


class User(db.Model):
    """User Model with necessary  fields"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
