from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from flask_login import UserMixin


class Base(DeclarativeBase):
    pass


# Person Model
class Person(UserMixin, Base):
    __tablename__ = "person_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    handle: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)
    hashed_password: Mapped[str] = mapped_column(String)
    joining_date: Mapped[str] = mapped_column(String)
    last_login: Mapped[str] = mapped_column(String)
    
    def __init__(self, first_name, last_name, handle, email, age, gender, phone_number, city, is_admin, hashed_password, joining_date, last_login):
        self.first_name = first_name
        self.last_name = last_name
        self.handle = handle
        self.email = email
        self.age = age
        self.gender = gender
        self.phone_number = phone_number
        self.city = city
        self.is_admin = is_admin
        self.hashed_password = hashed_password
        self.joining_date = joining_date
        self.last_login = last_login
        
    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}
 
 
 # User Model   
class User(UserMixin, Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(ForeignKey("person_table.id"), primary_key=True)
    level: Mapped[str] = mapped_column(String)
    
    person: Mapped["Person"] = relationship("Person", backref="user")
    group_id: Mapped[int] = mapped_column(ForeignKey("group_table.id"), nullable=True)
    group: Mapped["Group"] = relationship("Group", back_populates="members")
    
    def __init__(self, user_id, level, group=0):
        self.id = user_id
        self.level = level
        self.group_id = group
    
    def as_dict(self):
        return {**self.person.as_dict(), **{col.name: getattr(self, col.name) for col in self.__table__.columns}}

# Moderator Model
class Moderator(UserMixin, Base):
    __tablename__ = "moderator_table"

    id: Mapped[int] = mapped_column(ForeignKey("person_table.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group_table.id"))
    
    person: Mapped["Person"] = relationship("Person", backref="moderator")
    group: Mapped["Group"] = relationship("Group", back_populates="moderator")
    
    def __init__(self, moderator_id, group_id=0):
        self.id = moderator_id
        self.group_id = group_id
        
    def as_dict(self):
        return {**self.person.as_dict(), **{col.name: getattr(self, col.name) for col in self.__table__.columns}}


# Group Model
class Group(Base):
    __tablename__ = "group_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    members: Mapped[List["User"]] = relationship("User", back_populates="group", cascade="all, delete-orphan")
    moderator: Mapped["Moderator"] = relationship("Moderator", back_populates="group", uselist=False)
    
    def __init__(self, id):
        self.id = id

    def get_moderator(self):
        return self.moderator
    
    def set_moderator(self, moderator:Moderator):
        self.moderator=moderator
    
    def get_members(self):
        return self.members
    
    def set_members(self, members=list[User]):
        self.members=members

