"""
Flask creates the instance of WSGI application
"""
from flask import Flask, render_template

# from markupsafe import escape

app = Flask(__name__)


@app.route("/")
def index():
    """This view function is for the home page"""
    return render_template("index.html")


@app.route("/<cat>")
def topic(cat):
    """This view function is for Category posts page"""
    return render_template("topic.html", cat=cat)


@app.route("/submit")
def submit():
    """This view function is for the submit page"""
    return render_template("submit.html")


@app.route("/login")
def login():
    """This view function is for the submit page"""
    return render_template("login.html")


# html escaping
# @app.route("/<name>")
# def hello(name):
#     """Test function only"""
#     return f"I am {escape(name)}"
