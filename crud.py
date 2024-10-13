from model import Base, Person, User, Moderator, Admin, Group, Email
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///dk.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# first_name, last_name, handle, email, age, gender, phone_number, city, is_admin, password, joining_date, last_login
def create_person(*args, **kwargs):
    person = Person(*args)
    session.add(person)
    session.commit()


def create_user(*args, **kwargs):
    user = User(*args, **kwargs)
    session.add(user)
    session.commit()

def delete_user(user_id):
    stmt = delete(User).where(User.id==user_id)
    session.execute(stmt)
    session.commit()

def create_moderator(*args, **kwargs):
    moderator = Moderator(*args, **kwargs)
    session.add(moderator)
    session.commit()

def delete_moderator(moderator_id):
    stmt = delete(Moderator).where(Moderator.id==moderator_id)
    session.execute(stmt)
    session.commit()

def create_group(*args, **kwargs):
    group = Group(*args, **kwargs)
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
    

def delete_group(group_id):
    # changing group's moderator to default group
    change_group(Moderator, old_group_id=group_id, new_group_id=0)
    # changing group's member to default group
    change_group(User, old_group_id=group_id, new_group_id=0)
    
    stmt = delete(Group).where(Group.id==group_id)    
    session.execute(stmt)
    session.commit()

# create_person("Albert", "Twain", '1', '1', 35, '1', '1', '1', True, '1', '1', '1')

# stmt = select(Person).order_by(Person.id.desc())



for user_obj in result_table_by_id(User, 'id', 3):
    print(user_obj.person.first_name, user_obj.person.last_name)