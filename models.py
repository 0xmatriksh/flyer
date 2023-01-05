"""Models.py"""
from datetime import datetime
from app import db


class User(db.Model):
    """User Model with necessary  fields"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)


class Post(db.Model):
    """Post Model with necessary fields"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    source = db.Column(db.String, nullable=True)
    upvotes = db.Column(db.Integer, default=0)
    category = db.Column(db.String, nullable=True)
    comments = db.relationship("Comment", backref="post", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Comment(db.Model):
    """Comment Model with necessary fields"""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)
