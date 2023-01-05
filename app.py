"""
Flask creates the instance of WSGI application
"""
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

app.secret_key = "j54dsjdsd)021-jdsfjdkfddf?,/l.df"


from models import User, Post


@app.route("/")
def index():
    """This view function is for the home page"""
    # users = User.query.all()
    # for user in users:
    #     print(user.username)
    return render_template("index.html")


@app.route("/<cat>")
def topic(cat):
    """This view function is for Category posts page"""
    return render_template("topic.html", cat=cat)


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        author = User.query.filter_by(username=session["username"]).first()
        title = request.form["title"]
        content = request.form["content"]
        new_post = Post(title=title, content=content, author=author)
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
def logout():
    if "username" not in session:
        return redirect(url_for("login"))
    """function to logout the user by
    removing the user from the session"""
    session.pop("username", None)
    return redirect(url_for("index"))


# html escaping
# @app.route("/<name>")
# def hello(name):
#     """Test function only"""
#     return f"I am {escape(name)}"
