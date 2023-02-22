"""Models.py"""
from datetime import datetime


from app import db


class User(db.Model):
    """User Model with necessary  fields"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    upvotes = db.relationship("Upvote", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="author", lazy=True)
    cmnt_upvotes = db.relationship("CommentUpvote", backref="author", lazy=True)


class Post(db.Model):
    """Post Model with necessary fields"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    source = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=True)
    upvotes = db.relationship("Upvote", backref="post", lazy=True)
    comments = db.relationship("Comment", backref="post", lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Upvote(db.Model):
    """Upvote Model with necessary fields"""

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Comment(db.Model):
    """Comment Model with necessary fields"""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    upvotes = db.relationship("CommentUpvote", backref="comment", lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    created_at = db.Column(db.DateTime, default=datetime.now)
    replies = db.relationship(
        "Comment", backref=db.backref("parent", remote_side=[id]), lazy=True
    )


class CommentUpvote(db.Model):
    """Comments Upvote Model with necessary fields"""

    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
