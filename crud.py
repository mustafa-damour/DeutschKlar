from model import Base, Person, User, Moderator, Admin, Group
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import sessionmaker
import flask_bcrypt as bc
from datetime import datetime as dt

from logger import Logger

logger = Logger()

# library to get fake users/moderators
from faker import Faker
fake=Faker("de_DE")


engine = create_engine("sqlite:///dk.db", echo=False)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# first_name, last_name, handle, email, age, gender, phone_number, city, is_admin, hashed_password, joining_date, last_login
def create_person(person):
    session.add(person)
    session.commit()

# # first_name, last_name, handle, email, age, gender, phone_number, city, is_admin, hashed_password, joining_date, last_login
# def create_person(*args, **kwargs):
#     person = Person(*args)
#     session.add(person)
#     session.commit()


def create_user(person:Person, level:str):
    user = User(user_id=person.id, level=level)
    session.add(user)
    session.commit()

def delete_user(user_id):
    stmt = delete(User).where(User.id==user_id)
    session.execute(stmt)
    session.commit()

def create_moderator(person:Person, group_id:int=0):
    moderator = Moderator(moderator_id=person.id, group_id=group_id)
    session.add(moderator)
    session.commit()

def delete_moderator(moderator_id):
    stmt = delete(Moderator).where(Moderator.id==moderator_id)
    session.execute(stmt)
    session.commit()

### Deprecated
# def create_group(moderator: Moderator|None=None, members:list[User]|None=None):
#     group = Group()
#     if moderator:
#         group.moderator=moderator
#     if members:
#         group.members=members
#     session.add(group)
#     session.commit()
    
def create_group(group:Group):
    session.add(group)
    session.commit()

    
def create_email(*args, **kwargs):
    email = Email(*args, **kwargs)
    session.add(email)
    session.commit()

def change_group(Table:User|Moderator|Admin, old_group_id, new_group_id):
    select_stmt = select(Table).where(Table.group_id == old_group_id)
    result = session.execute(select_stmt)
    for table_obj in result.scalars():
        update_stmt = update(Table).where(Table.id == table_obj.id).values(group_id=new_group_id)
        session.execute(update_stmt)
        session.commit()

def result_table_by_id(Table:User|Moderator|Admin, id_name:str, id_value:str):
    if id_name == 'group_id':
        stmt = select(Table).where(Table.group_id==id_value)
    else:
        stmt = select(Table).where(Table.id==id_value)
    result = session.execute(stmt)
    return result.scalars()

def get_person_by_handle(Table:User|Moderator|Admin, handle: str):

    result = session.query(Person).join(Table).filter(Person.handle == handle)    
    return result.first()


def delete_group(group_id):
    # changing group's moderator to default group
    change_group(Moderator, old_group_id=group_id, new_group_id=0)
    # changing group's member to default group
    change_group(User, old_group_id=group_id, new_group_id=0)
    
    stmt = delete(Group).where(Group.id==group_id)    
    session.execute(stmt)
    session.commit()
    
def get_user(user_id):
    return  session.query(User).filter(User.id==user_id).first()

def get_group(group_id):
    return  session.query(Group).filter(Group.id==group_id).first()

def get_moderator(moderator_id):
    return  session.query(Moderator).filter(Moderator.id==moderator_id).first()

def get_group_moderator(group_id):
    return  session.query(Moderator).filter(Moderator.group_id==group_id).first()

def get_group_members(group_id):
    return  session.query(User).filter(User.group_id==group_id).all()

def get_waitlist():
    return get_group_members(group_id=0)


# for user in get_group_members(group_id=0):
#     try:
#         person = user.person
#         logger.log(f"Id:{person.id}, first name:{person.first_name}")
#     except:
#         logger.log("User doesn't exist")

CITIES = ['Cairo', 'Alexandria', 'Sinai','Luxor','Aswan','Sohag','Manofia','Asyut','Ismailia']
LEVELS = ['A0', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']

def get_city_id(city:str):
    return 1+CITIES.index(city)

        
def generate_cities_persons(role:Person|User|Moderator, cities:list[str]=[]):
    for city in cities:
        person = Person(
            first_name=fake.first_name_female(),
            last_name=fake.last_name(),
            handle=fake.first_name(),
            email=fake.email(),
            age=fake.random_element([21,42,35]),
            gender='famale',
            phone_number=fake.phone_number(),
            city=city,
            is_admin=False,
            hashed_password=fake.password(),
            joining_date=fake.date_this_decade(),
            last_login=fake.date_this_month()
        )
        
        create_person(person=person)
        city_id=get_city_id(city=city)
        logger.log(f">>>>>>>>>>>>>> Role = {role.__tablename__}, City ID = {city_id}")
        try:
            city_group = get_group(group_id=city_id)
        except:
            city_group = Group(id=city_id)
            create_group(group=city_group)
            city_group = get_group(group_id=city_id)
        if role.__tablename__=="user_table":
            create_user(person=person, level=fake.random_element(LEVELS))
            new_user = get_user(user_id=person.id)
            
            city_group = get_group(group_id=city_id)
            
            try:
                city_group.members.append(new_user)
            except:
                # stmt = update(Group)\
                # .where(Group.id==city_id)\
                # .values(members=[new_user])
                
                # session.execute(stmt)
                city_group.set_members([new_user])
                session.commit()
                
            new_user.group_id=city_id
            session.commit()
            
        elif role.__tablename__=="moderator_table":
            city_group = get_group(group_id=city_id)
            create_moderator(person=person, group_id=city_id)
            new_moderator = get_moderator(moderator_id=person.id)
            city_group.set_moderator(new_moderator)
            new_moderator.group_id=city_id
            session.commit()
        

def initialize_groups():
    for i in range(1, 1+len(CITIES)):
        group=get_group(group_id=i)
            
        if not group:
            group = Group(id=i)
            create_group(group=group)


def update_user_lastlogin(user:User):
    user.person.last_login=dt.now().strftime("%m/%d/%Y, %H:%M:%S")
    session.commit()


def match_user(user: User):
    user_city = user.person.city
    user.group_id = get_city_id(user_city)
    city_group = get_group(user.group_id)
    city_group.members.append(user)
    session.commit()