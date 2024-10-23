import flask
from flask import request
from flask_mail import Mail,Message
import flask_bcrypt as bc
from model import User, Person
from crud import get_user, create_person, create_user, match_user, update_user_lastlogin
import crud
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime as dt
import secrets
from logger import Logger
import json

logger = Logger()

MAIL_PASSWORD = 'vfjy edir ovze eptu'

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
# setting login_view
login_manager.login_view = 'login'


# Basic configs to allow for Email service
app.config.update(
  DEBUG=True,
  #EMAIL SETTINGS
  MAIL_SERVER='smtp.gmail.com',
  MAIL_PORT=465,
  MAIL_USE_SSL=True,
  MAIL_USERNAME = 'DeutschKlar.rc',
  MAIL_PASSWORD = MAIL_PASSWORD
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
    content = get_html('site/about')
    return content

@app.route("/faqs")
def faqs():
    return get_html('site/faqs')

@app.route("/inout")
def inout():
    if current_user.is_authenticated:
        return app.redirect('/logout')
    else:
        return app.redirect('/login')

@app.route("/logs")
@login_required
def logs():
    with app.app_context():
        user_id = current_user.id
        user = get_user(user_id=user_id)
        if user.person.is_admin:
            logger.log(f'Admin logged in')
            content = get_html('site/admin/logs')
            return content
        else:
            return app.redirect('/dashboard')

@app.route("/get_logs")
@login_required
def get_logs():
    with app.app_context():
        user_id = current_user.id
        user = get_user(user_id=user_id)
        if user.person.is_admin:
            logs = logger.get_last_n_logs(20).split('\n');
            return json.dumps(logs)
        else:
            return ""

@app.route("/delete_logs")
@login_required
def delete_logs():
    with app.app_context():
        user_id = current_user.id
        user = get_user(user_id=user_id)
        if user.person.is_admin:
            logger.clear_logs()
            return app.redirect('/logs')
        else:
            return app.redirect('/dashboard')

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
            stored_hashed_password = crud.get_person_by_handle(Table=User, handle=handle).hashed_password
            if bc.check_password_hash(stored_hashed_password, password):    
                login_user(user, remember=True)
                update_user_lastlogin(user)

                logger.log(f'User with id=[{user.person.id}] logged in')

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
    if current_user.is_authenticated:
        with app.app_context():
            user_id = current_user.id
            user = get_user(user_id=user_id)
            logger.log(f'User with id=[{user.person.id}] logged out')
    logout_user()
    return app.redirect('/login')


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
        hashed_password=bc.generate_password_hash(data['password']),
        joining_date=str(dt.now().strftime("%d/%m/%Y %H:%M:%S")),
        last_login=''
    )
    try:
        create_person(person)
        create_user(person=person, level=data['level'])
        user = get_user(person.id)
        logger.log(f'New User created, id=[{user.person.id}]')    
        # print(person.phone_number)
        email(title='Confirmation of Registeration', body='', html=reg_html, recipients=[data['email']])
        
        match_user(user=user)
        email(title="Successful Matching", body="You've been successfully matched with a group, check your dashboard.", html='', recipients=[data['email']])
            
        return app.redirect('/login')
    except:
        return get_html('site/register')+'<script>alert("please change handle and/or emails");</script>'


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
        
        user_json = {
            'user':  {
            'handle': user.person.handle,
            'first_name': user.person.first_name,
            'last_name': user.person.last_name,
            'email': user.person.email,
            'user_id': user.person.id
            }
        }
        
        json_data = {}
        moderator_json={'moderator':moderator.as_dict()}
        moderator_json['moderator'].pop('hashed_password')
        members_json = {}
        members_json['members']={}

        for member in members:
            member_as_value = member.as_dict()
            member_as_value.pop('hashed_password')
            members_json['members']={**members_json['members'], **{member.person.handle:member_as_value}}
        
        json_data = {**user_json, **moderator_json, **members_json}

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