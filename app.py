"""
Flask creates the instance of WSGI application
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime
from flask_humanize import Humanize
from functools import wraps
from utils.algo import predict_cat
from dotenv import load_dotenv
from sqlalchemy import func, desc

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
humanize = Humanize(app)
load_dotenv()

HUMANIZE_USE_UTC = True

app.secret_key = os.environ.get("SECRET_KEY")

from models import User, Post, Upvote, Comment, CommentUpvote


def login_required(func):
    """decorator function to check if the user is logged in or not"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if "username" in session:
            user = User.query.filter_by(username=session["username"]).first()
            if not user:
                session.pop("username", None)
                return redirect(url_for("login"))
            else:
                return func(*args, **kwargs)
        else:
            return redirect(url_for("login"))

    return wrapper


def category_map(idx):
    if idx in [16, 17, 18]:
        return "Politics"
    elif idx in [1, 2, 3, 4, 5, 12]:
        return "Tech"
    elif idx in [11, 13, 14]:
        return "Science"
    elif idx in [15, 0, 19]:
        return "Social"
    elif idx in [10, 9]:
        return "Sports"
    else:
        return "Misc"


@app.route("/")
def index():
    """This view function is for the home page"""
    # users = User.query.all()
    # for user in users:
    #     print(user.username)
    pagenum = request.args.get("page", 1, type=int)
    page = (
        Post.query.outerjoin(Upvote)  # outerjoin to not discard posts with no upvotes
        .outerjoin(Comment)
        .group_by(Post.id)
        .order_by(desc(db.func.count(Upvote.id) + db.func.count(Comment.id)))
        .paginate(page=pagenum, per_page=10)
    )
    # page = Post.query.paginate(page=pagenum, per_page=10)
    posts = page.items
    now = datetime.now()
    upvoted_posts = []
    karma = 0
    if "username" in session:
        author = User.query.filter_by(username=session["username"]).first()

        # karma of the posts by this user
        karma = (
            db.session.query(func.count(Upvote.id))  # counts all the upvotes
            .join(Post)  # joins upvotes with Post
            .filter(Post.author_id == author.id)  # get posts by this user
            .scalar()  # if no found, scalar() returns None
        ) or 0
        for post in posts:
            upvote = Upvote.query.filter_by(
                post_id=post.id, author_id=author.id
            ).first()
            if upvote:
                upvoted_posts.append(post.id)

    return render_template(
        "index.html",
        karma=karma,
        posts=posts,
        page=page,
        now=now,
        upvoted_posts=upvoted_posts,
    )


@app.route("/new")
def new():
    """This view function is for the home page"""
    # users = User.query.all()
    # for user in users:
    #     print(user.username)
    pagenum = request.args.get("page", 1, type=int)
    page = Post.query.order_by(desc(Post.created_at)).paginate(
        page=pagenum, per_page=10
    )
    # page = Post.query.paginate(page=pagenum, per_page=10)
    posts = page.items
    now = datetime.now()
    upvoted_posts = []
    karma = 0
    if "username" in session:
        author = User.query.filter_by(username=session["username"]).first()

        # karma of the posts by this user
        karma = (
            db.session.query(func.count(Upvote.id))  # counts all the upvotes
            .join(Post)  # joins upvotes with Post
            .filter(Post.author_id == author.id)  # get posts by this user
            .scalar()  # if no found, scalar() returns None
        ) or 0
        for post in posts:
            upvote = Upvote.query.filter_by(
                post_id=post.id, author_id=author.id
            ).first()
            if upvote:
                upvoted_posts.append(post.id)

    return render_template(
        "index.html",
        karma=karma,
        posts=posts,
        page=page,
        now=now,
        upvoted_posts=upvoted_posts,
    )


@app.route("/<cat>")
def topic(cat):
    category = cat.title()
    # posts = Post.query.filter_by(category=category).all()
    page = (
        Post.query.outerjoin(Upvote)
        .outerjoin(Comment)
        .filter(Post.category == category)
        .group_by(Post.id)
        .order_by(desc(db.func.count(Upvote.id) + db.func.count(Comment.id)))
        .paginate(page=1, per_page=10)
    )
    posts = page.items
    now = datetime.now()
    upvoted_posts = []
    if "username" in session:
        author = User.query.filter_by(username=session["username"]).first()
        for post in posts:
            upvote = Upvote.query.filter_by(
                post_id=post.id, author_id=author.id
            ).first()
            if upvote:
                upvoted_posts.append(post.id)
    """This view function is for Category posts page"""
    return render_template(
        "topic.html",
        cat=cat,
        category=category,
        posts=posts,
        page=page,
        now=now,
        upvoted_posts=upvoted_posts,
    )


@app.route("/<cat>/new")
def topicnew(cat):
    category = cat.title()
    # posts = Post.query.filter_by(category=category).all()
    page = (
        Post.query.filter_by(category=category)
        .order_by(desc(Post.created_at))
        .paginate(page=1, per_page=10)
    )
    posts = page.items
    now = datetime.now()
    upvoted_posts = []
    if "username" in session:
        author = User.query.filter_by(username=session["username"]).first()
        for post in posts:
            upvote = Upvote.query.filter_by(
                post_id=post.id, author_id=author.id
            ).first()
            if upvote:
                upvoted_posts.append(post.id)
    """This view function is for Category posts page"""
    return render_template(
        "topic.html",
        category=category,
        posts=posts,
        page=page,
        now=now,
        upvoted_posts=upvoted_posts,
    )


@app.route("/post/<postid>")
@login_required
def post(postid):
    """This view function is for Post detail"""
    now = datetime.now()
    upvoted = False
    author = User.query.filter_by(username=session["username"]).first()
    post = Post.query.filter_by(id=postid).first()
    upvote = Upvote.query.filter_by(post_id=post.id, author_id=author.id).first()
    if upvote:
        upvoted = True
    comments = Comment.query.filter_by(post_id=post.id, parent_id=None).all()
    allcomments = Comment.query.filter_by(post_id=post.id)
    upvoted_comments = []
    if "username" in session:
        author = User.query.filter_by(username=session["username"]).first()
        for comment in allcomments:
            upvote = CommentUpvote.query.filter_by(
                comment_id=comment.id, author_id=author.id
            ).first()
            if upvote:
                upvoted_comments.append(comment.id)

    return render_template(
        "post.html",
        now=now,
        post=post,
        comments=comments,
        upvoted=upvoted,
        upvoted_comments=upvoted_comments,
    )


@app.route("/comment/<postid>", methods=["GET", "POST"])
@login_required
def comment(postid):
    text = request.form.get("text")
    author = User.query.filter_by(username=session["username"]).first()
    new_comment = Comment(
        text=text, author_id=author.id, post_id=postid, parent_id=None
    )
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("post", postid=postid))


# this is api only can return json
@app.route("/reply/<post_id>/<parent_id>", methods=["GET", "POST"])
def reply(post_id, parent_id):
    if request.method == "POST":
        # add this reply to comment from user to database
        reply = request.form["cmnt"]
        author = User.query.filter_by(username=session["username"]).first()

        print("Comment from user")
        print("Parent id: ", parent_id)
        print("Reply text: ", reply)
        new_reply = Comment(
            text=reply, author_id=author.id, post_id=post_id, parent_id=parent_id
        )

        db.session.add(new_reply)
        db.session.commit()

    else:
        print("Nothing")
    return redirect(url_for("post", postid=post_id))


@app.route("/like/<postid>")
@login_required
def like(postid):
    post = Post.query.filter_by(id=postid).first()
    author = User.query.filter_by(username=session["username"]).first()
    upvotes = Upvote.query.filter_by(post=post, author=author).all()
    if len(upvotes) == 0:
        new_like = Upvote(author=author, post=post)
        db.session.add(new_like)
        db.session.commit()
    else:
        print(upvotes)
        print("There is already likes by this user")
    return redirect(url_for("index"))


@app.route("/unlike/<postid>")
@login_required
def unlike(postid):
    post = Post.query.filter_by(id=postid).first()
    author = User.query.filter_by(username=session["username"]).first()
    upvote = Upvote.query.filter_by(post=post, author=author).all()
    if len(upvote) != 0:
        db.session.delete(upvote[0])
        db.session.commit()
    else:
        print(upvote)
        print("There is no upvote by this user, then how can delete, HUH?")
    return redirect(url_for("index"))


@app.route("/cmntupvote/<cmntid>")
@login_required
def cmntupvote(cmntid):
    comment = Comment.query.filter_by(id=cmntid).first()
    author = User.query.filter_by(username=session["username"]).first()
    upvotes = CommentUpvote.query.filter_by(comment=comment, author=author).all()
    if len(upvotes) == 0:
        new_like = CommentUpvote(author=author, comment=comment)
        db.session.add(new_like)
        db.session.commit()
    else:
        print("There is already likes by this user")
    return redirect(url_for("index"))


# this is api only can return json
@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    """This view function is for the post submit page"""

    if request.method == "POST":
        author = User.query.filter_by(username=session["username"]).first()
        title = request.form["title"]
        content = request.form["content"]

        total = title + " " + content
        idx = predict_cat(total)
        # print(category_map(idx))

        new_post = Post(
            title=title, content=content, author=author, category=category_map(idx)
        )
        db.session.add(new_post)
        db.session.commit()
        print("Post Added")
        return redirect(url_for("index"))
    return render_template("submit.html")


@app.route("/edit/<int:postid>", methods=["GET", "POST"])
@login_required
def edit(postid):
    """This view function is for the post edit page"""

    post = Post.query.filter_by(id=postid).first()
    if request.method == "POST":
        author = User.query.filter_by(username=session["username"]).first()
        if post and post.author == author:
            db.session.delete(post)
            db.session.commit()

            author = User.query.filter_by(username=session["username"]).first()
            title = request.form["title"]
            content = request.form["content"]
            idx = predict_cat(title)
            new_post = Post(
                id=postid,
                title=title,
                content=content,
                author=author,
                category=category_map(idx),
            )
            db.session.add(new_post)
            db.session.commit()
            print("Post Added")
            return redirect(url_for("index"))
    return render_template("edit.html", post=post)


@app.route("/login", methods=["GET", "POST"])
def login():
    """This view function is for the login page"""

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            # login successful
            session["username"] = username
            return redirect(url_for("index"))
        else:
            # login failed
            return render_template("login.html", error=True)
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """function to create an account"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password)
        new_user = User(username=username, password=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    """function to logout the user by
    removing the user from the session"""
    session.pop("username", None)
    return redirect(url_for("index"))


# html escaping
# @app.route("/<name>")
# def hello(name):
#     """Test function only"""
#     return f"I am {escape(name)}"
