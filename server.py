import flask
from flask import request
# import model as orm
# import crud

from enum import Enum


app = flask.Flask("DeutschKlar")


### Creating an Enum class for case-by-case selection
# class Person(Enum):
#     USER=1
#     MODERATOR=2
#     ADMIN=3


def get_html(file):
    f = open(f'{file}.html')
    content = f.read()
    return content

@app.route("/")
@app.route("/home")
def homepage():
    return "home"

@app.route("/about")
def about():
    return "about"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        handle = request.form.get('handle')
        password = request.form.get('password')
        print(*zip(request.form.keys(), request.form.values()), sep='\n')
        # print(f"the handle is {handle} and the passowrd is {password}")
        return app.redirect('/')
    else:
        return get_html('site/login')

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
