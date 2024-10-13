import flask
app = flask.Flask("DeutschKlar")

import model as orm
import crud

@app.route("/")
@app.route("/home")
def homepage():
    return "home"

@app.route("/about")
def about():
    return "about"

@app.route("/login")
def login():
    return "login"

@app.route("/logout")
def logout():
    return "logout"

@app.route("/group")
def group():
    return "group"

@app.route("/groups")
def groups():
    return "groups"

@app.route("/message")
def message():
    return "message"
