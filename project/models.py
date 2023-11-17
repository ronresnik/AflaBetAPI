
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, ARRAY
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash
import re
from validate_email_address import validate_email
from project import db


user_event_association = db.Table(
    'user_event_association',
    db.Column('user_id', Integer, ForeignKey('users.id')),
    db.Column('event_id', Integer, ForeignKey('events.id'))
)


class User(UserMixin, db.Model):

    """
    Class that represents a user of the application

    The following attributes of a user are stored in this table:
        * email - email address of the user
        * hashed password - hashed password (using werkzeug.security)
        * registered_on - date & time that the user registered

    """

    __tablename__ = 'users'

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    email = mapped_column(String(), unique=True, nullable=False)
    password_hashed = mapped_column(String(128), nullable=False)
    registered_on = mapped_column(DateTime(), nullable=False)
    events = relationship(
        'Event', secondary=user_event_association)

    def __init__(self, email: str, password_plaintext: str):
        """Create a new User object using the email address and hashing the
        plaintext password using Werkzeug.Security.
        """
        if not self._is_valid_email(email):
            raise ValueError("Invalid email address.")

        if not self._is_valid_password(password_plaintext):
            raise ValueError(
                "Invalid password. It must have one special character, only ASCII characters, at least one number, at least one uppercase and one lowercase character, and a length between 8 and 20.")

        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()

    def _is_valid_email(self, email):
        return validate_email(email)

    def _is_valid_password(self, password):
        # Password must have one special character, only ASCII characters,
        # at least one number, at least one uppercase and one lowercase character,
        # and a length between 8 and 20.
        regex = re.compile(r'^(?=.*[!@#$%^&*()_+{}|:"<>?])'
                           r'(?=.*[0-9])'
                           r'(?=.*[a-z])'
                           r'(?=.*[A-Z])'
                           r'[A-Za-z0-9!@#$%^&*()_+{}|:<>?]{8,20}$')
        return bool(regex.match(password))

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<User: {self.email}>'


class Event(db.Model):
    __tablename__ = 'events'

    id = mapped_column(Integer(), primary_key=True, autoincrement=True)
    title = mapped_column(String(255), unique=True, nullable=False)
    description = mapped_column(String(255), nullable=False)
    venue = mapped_column(String(255), nullable=False)
    location = mapped_column(String(255), nullable=False)
    event_date = mapped_column(DateTime(), nullable=False)
    tags = mapped_column(ARRAY(String(50)), nullable=True)
    participants = mapped_column(Integer(), default=1)
    created_at = mapped_column(DateTime(), default=func.now())

    # subscribers = relationship(
    #     'User', secondary=user_event_association, back_populates='events') TODO Implement

    def __init__(self, title, description, venue, location, event_date, tags=None, participants=1):
        if not title or len(title) < 5 or len(title) > 255:
            raise ValueError(
                "Title must be non-empty and between 5 and 255 characters long.")

        if not description or len(description) < 5 or len(description) > 255:
            raise ValueError(
                "Description must be non-empty and between 5 and 255 characters long.")

        if not venue or len(venue) < 5 or len(venue) > 255:
            raise ValueError(
                "Venue must be non-empty and between 5 and 255 characters long.")

        if not location or len(location) < 5 or len(location) > 255:
            raise ValueError(
                "Venue must be non-empty and between 5 and 255 characters long.")

        if event_date < datetime.now():
            raise ValueError("Event date cannot be in the past.")

        if participants is not None and participants < 1:
            raise ValueError(
                "Participants must be greater than or equal to 1.")

        self.title = title
        self.description = description
        self.venue = venue
        self.location = location
        self.event_date = event_date
        self.tags = tags if tags is not None else []
        self.participants = participants

    def __repr__(self):
        return f'<Event: {self.title} - {self.event_date}>'
