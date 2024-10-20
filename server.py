import flask
from flask import request
from flask_mail import Mail,Message
from model import User
from crud import get_user
import crud
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime
import secrets
# import smtplib
import asyncio
# import random

secret_key = secrets.token_hex(16)


# secret_key = '2342342dfgsdfg'


app = flask.Flask("DeutschKlar")

app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)


app.config.update(
  DEBUG=True,
  #EMAIL SETTINGS
  MAIL_SERVER='smtp.gmail.com',
  MAIL_PORT=465,
  MAIL_USE_SSL=True,
  MAIL_USERNAME = 'DeutschKlar.rc',
  MAIL_PASSWORD = 'vfjy edir ovze eptu'
)

mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)


def get_html(file):
    f = open(f'{file}.html', encoding="utf8")
    content = f.read()
    return content

@app.route("/")
@app.route("/home")
def homepage():
    content = get_html('site/index')
    return content

@app.route("/about")
def about():
    return "about"



@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        handle = request.form.get('handle')
        password = request.form.get('password')
        try:
            user_id = crud.get_person_by_handle(Table=User, handle=handle).id
            user:User = crud.get_user(user_id=user_id)
        except:
            return get_html('site/login')
        try:
            stored_password = crud.get_person_by_handle(Table=User, handle=handle).password
            if stored_password==password:    
                login_user(user, remember=True)
                print(current_user)
                return app.redirect('/dashboard')
            else:
                return get_html('site/home')
        except Exception as e:
            print(e)
            return e.__repr__()
    elif current_user.is_authenticated :
        return app.redirect('/dashboard')    
    else:
        return get_html('site/login')



@app.route("/logout")
def logout():
    logout_user()
    return app.redirect('/login')

@app.route("/group")
def group():
    return "group"

@app.route("/register", methods=['GET'])
def register():
    return get_html('site/register')

@app.route("/create", methods=['POST'])
def create():
    data = request.form.to_dict()

    return str(data)

@app.route("/message")
@login_required
def message():
    return "message"

@app.route("/dashboard")
@login_required
def user_dashboard():
    return get_html('site/user/dashboard')


reg_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirmation of Registeration</title>
</head>
<body>
    
<style>
    .card-container {
      display:flex;
      justify-content: center;
      align-items: center;
      padding: 12px;
      width:100%;
      height:100%;
    }
    
    .card {
      height: 50%;
      width: 50%;
      background-color:light;
      padding: 16px;
      box-shadow: rgba(0, 0, 0, 0.15) 0px 2px 8px;
    
    }
    
    h1 {
      font-family: "Helvetica";
      font-weight: bold;
      color: darkred;
    }
    
    p {
     font-size: 24px;
     font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    </style>
     
    <div class="card-container">
      <div class="card">
        <h1><em>Danke!</em> Für deine Abmeldung bei DeutschKlar</h1>
        <p>Thank you for registering with DeutschKlar, your journey starts now</p>
        <p>We attached a PDF document containing all the infomation you might want to know about DeutschKlar, and how to get the most out of it.</p>
        <h1>Viel Spaß</h1>
      </div>
    </div>
    
</body>
</html>
"""

def email(title: str, body:str, html: str, recipients: list[str]):
  with app.app_context():
    try:
        msg = Message(title, sender="deutschkalr.rc@gmail.com", recipients=recipients)
        msg.body = body
        if html:        
            msg.html = html
        if title == 'Confirmation of Registeration':
            with app.open_resource("Brochure.pdf") as fp:
                msg.attach("Brochure.pdf", "application/pdf", fp.read())
        
        mail.send(msg)
        return 'Mail Send Successfully'
        
    except Exception as e:
        print('***** '+str(e))
    return ""

# print(email("Confirmation of Registeration", "", reg_html,recipients=['damour91919@gmail.com']))