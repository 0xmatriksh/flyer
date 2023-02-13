"""
Flask creates the instance of WSGI application
"""
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime
from flask_humanize import Humanize
from functools import wraps
from algo import predict

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
humanize = Humanize(app)


HUMANIZE_USE_UTC = True


app.secret_key = "j54dsjdsd)021-jdsfjdkfddf?,/l.df"


from models import User, Post, Upvote, Comment


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
    elif idx in [7, 8]:
        return "Auto"
    else:
        return "Misc"


@app.route("/")
def index():
    """This view function is for the home page"""
    # users = User.query.all()
    # for user in users:
    #     print(user.username)
    posts = Post.query.all()
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

    return render_template(
        "index.html", posts=posts, now=now, upvoted_posts=upvoted_posts
    )


@app.route("/<cat>")
def topic(cat):
    """This view function is for Category posts page"""
    return render_template("topic.html", cat=cat)


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
    # not equals to check to get replies only
    # replies = Comment.query.filter_by(post_id=post.id).all()
    return render_template(
        "post.html",
        now=now,
        post=post,
        comments=comments,
        upvoted=upvoted,
        # replies=replies,
    )


@app.route("/comment/<postid>", methods=["GET", "POST"])
@login_required
def comment(postid):
    text = request.form["text"]
    author = User.query.filter_by(username=session["username"]).first()
    new_comment = Comment(
        text=text, author_id=author.id, post_id=postid, parent_id=None
    )
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("post", postid=postid))


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


@app.route("/submit", methods=["GET", "POST"])
@login_required
def submit():
    if request.method == "POST":
        author = User.query.filter_by(username=session["username"]).first()
        title = request.form["title"]
        content = request.form["content"]
        idx = predict(content)
        new_post = Post(
            title=title, content=content, author=author, category=category_map(idx)
        )
        db.session.add(new_post)
        db.session.commit()
        print("Post Added")
        return redirect(url_for("index"))
    """This view function is for the submit page"""
    return render_template("submit.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """This view function is for the submit page"""
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
