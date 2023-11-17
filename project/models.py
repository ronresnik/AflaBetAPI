
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, ARRAY
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

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
        self.email = email
        self.password_hashed = self._generate_password_hash(password_plaintext)
        self.registered_on = datetime.now()

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
    description = mapped_column(String(255), unique=True, nullable=True)
    venue = mapped_column(String(255), nullable=True)
    event_date = mapped_column(DateTime(), nullable=False)
    tags = mapped_column(ARRAY(String(50)), nullable=True)
    participants = mapped_column(Integer(), default=0)
    created_at = mapped_column(DateTime(), default=func.now())
    # subscribers = relationship(
    #     'User', secondary=user_event_association, back_populates='events') TODO Implement

    def __init__(self, title, description, venue, event_date, tags=None, participants=1):
        self.title = title
        self.description = description
        self.venue = venue
        self.event_date = event_date
        self.tags = tags if tags else []
        self.participants = participants

    def update_event(self, title=None, description=None, venue=None, event_date=None, tags=None):
        if title:
            self.title = title
        if description:
            self.description = description
        if venue:
            self.venue = venue
        if event_date:
            self.event_date = event_date
        if tags is not None:
            self.tags = tags

    def __repr__(self):
        return f'<Event: {self.title} - {self.event_date}>'
