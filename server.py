import flask
from flask import request
from model import User
from crud import get_user
import crud
from flask_login import LoginManager, login_user, logout_user, login_required
import secrets

secret_key = secrets.token_hex(16)


app = flask.Flask("DeutschKlar")

app. secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


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

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     if request.method=='POST':
#         handle = request.form.get('handle')
#         password = request.form.get('password')
#         try:
#             stored_password = crud.get_password_by_handle(Table=User, handle=handle).password
#             if stored_password==password:
#                 return app.redirect('/')
#         except:
#             return get_html('site/login')
        
#     else:
#         return get_html('site/login')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        handle = request.form.get('handle')
        password = request.form.get('password')
        user_id = crud.get_person_by_handle(Table=User, handle=handle).id
        user:User = crud.get_user(user_id=user_id)
        try:
            stored_password = crud.get_person_by_handle(Table=User, handle=handle).password
            if stored_password==password:    
                login_user(user)
                return 'HI'
            else:
                return get_html('site/home')
        except Exception as e:
            print(e)
            return e.__repr__()
        
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
