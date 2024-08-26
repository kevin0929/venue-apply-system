import enum

from sqlalchemy import Column, Enum, Integer, MetaData, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

"""
This file is focus on
The schema of every table in database
"""

Base = declarative_base(metadata=MetaData())


class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("username"), UniqueConstraint("email"))

    # Relationships with applicaion
    applications = relationship("Application", back_populates="user")


class Venue(Base):
    __tablename__ = "venue"

    vid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    # Relationships with applicaion
    applications = relationship("Application", back_populates="venue")


class Application(Base):
    __tablename__ = "application"

    aid = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    vid = Column(Integer, ForeignKey("venue.vid"), nullable=False)
    datetime = Column(String, nullable=False)
    order = Column(Integer, nullable=False)

    '''
    Relationships
    user : one-to-many
    venue: one-to-many
    '''
    user = relationship("User", back_populates="applications")
    venue = relationship("Venue", back_populates="applications")
