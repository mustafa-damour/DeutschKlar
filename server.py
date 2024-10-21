import flask
from flask import request
from flask_mail import Mail,Message
from model import User, Person
from crud import get_user, create_person, create_user, match_user
import crud
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime as dt
import secrets

## Generating secret key for the server, a new one is generated each time the server is restarted, and users are
## automatically logged-out
secret_key = secrets.token_hex(16)

## Creating Flask app instance
app = flask.Flask("DeutschKlar")

# setting secret_key for the server
app.secret_key = secret_key

# Creating an instance of the LoginManager, and connecting it to the app
login_manager = LoginManager()
login_manager.init_app(app)


# Basic configs to allow for Email service
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

# Email loader to allow for fetching user form DB
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
    content = get_html('site/index')
    return content



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
                return get_html('site/login')
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
    person = Person(
        first_name=data['fname'],
        last_name=data['lname'],
        handle=data['handle'],
        email=data['email'],
        age=data['age'],
        gender=data['gender'],
        phone_number=data['phone_number'],
        city=data['city'],
        is_admin=False,
        password=data['password'],
        joining_date=str(dt.now().strftime("%d/%m/%Y %H:%M:%S")),
        last_login=''
    )
    create_person(person)
    create_user(person=person, level=data['level'])
    user = get_user(person.id)
    match_user(user=user)
    
    # print(person.phone_number)
    email(title='Confirmation of Registeration', body='', html=reg_html, recipients=[data['email']])
    return app.redirect('/login')

@app.route("/message")
@login_required
def message():
    return "message"

@app.route("/dashboard", methods=['GET'])
@login_required
def user_dashboard():
    return get_html('site/user/dashboard')

@app.route("/cards", methods=['GET'])
@login_required
def cards():
    with app.app_context():
        user_id = current_user.id
        user = get_user(user_id=user_id)
        user_group = user.group
        moderator = user_group.moderator
        members=user_group.members
    
        json_data = {}
        moderator_json={'moderator':moderator.as_dict()}

        members_json = {}

        for member in members:
            members_json[member.person.handle]=member.as_dict()
        
        json_data = {**moderator_json, **members_json}

        return json_data

reg_html = get_html('email')

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
        print(str(e))
    return ""

# print(email("Confirmation of Registeration", "", reg_html,recipients=['damour91919@gmail.com']))