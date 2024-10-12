from __future__ import annotations
from typing import List

from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "person_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    handle: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    gender: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)
    password: Mapped[str] = mapped_column(String)
    joining_date: Mapped[str] = mapped_column(String)
    last_login: Mapped[str] = mapped_column(String)

class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    level: Mapped[str] = mapped_column(String)
    
    group_id: Mapped[int] = mapped_column(ForeignKey("group_table.id"))
    group: Mapped["Group"] = relationship("Group", back_populates="members")

class Moderator(Base):
    __tablename__ = "moderator_table"

    id: Mapped[int] = mapped_column(ForeignKey("person_table.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group_table.id"))
    
    person: Mapped["Person"] = relationship("Person", backref="moderator")
    group: Mapped["Group"] = relationship("Group", back_populates="moderator")

class Admin(Base):
    __tablename__ = "admin_table"

    id: Mapped[int] = mapped_column(ForeignKey("person_table.id"), primary_key=True)
    title: Mapped[str] = mapped_column(String)
    
    person: Mapped["Person"] = relationship("Person", backref="admin")

class Group(Base):
    __tablename__ = "group_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    members: Mapped[List["User"]] = relationship("User", back_populates="group", cascade="all, delete-orphan")
    moderator: Mapped["Moderator"] = relationship("Moderator", back_populates="group", uselist=False)
class Email(Base):
    __tablename__ = "email_table"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    message: Mapped[str] = mapped_column(String)
    date: Mapped[str] = mapped_column(String)

