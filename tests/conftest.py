from datetime import datetime
import os

import pytest

from project import create_app, db
from project.models import Event, User


# --------
# Fixtures
# --------

@pytest.fixture(scope='module')
def new_user():
    user = User('ronresnik79@gmail.com', 'SummerIsAwesome')
    return user


@pytest.fixture(scope='module')
def client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


@pytest.fixture(scope='module')
def init_database(client):
    # Create the database and the database table
    db.drop_all()
    db.create_all()

    # Insert user data
    default_user = User(email='ronresnik79@gmail.com',
                        password_plaintext='SummerIsAwesome')
    second_user = User(email='ron@yahoo.com',
                       password_plaintext='SummerIsTheBest987')
    db.session.add(default_user)
    db.session.add(second_user)

    # Commit the changes for the users
    db.session.commit()

    # Insert Event Data
    event1 = Event('Event 1 Title', 'Description 1', 'Venue 1', datetime(
        2023, 9, 17, 18, 0, 0), ['Tag1', 'Tag2'], participants=10)
    event2 = Event('Event 2 Title', 'Description 2', 'Venue 2', datetime(
        2023, 9, 18, 19, 30, 0), ['Tag3', 'Tag4'], participants=20)
    event3 = Event('Event 3 Title', 'Description 3', 'Venue 3', datetime(
        2023, 9, 19, 15, 45, 0), ['Tag5', 'Tag6'], participants=15)
    default_user.events.append(event1)
    default_user.events.append(event2)
    default_user.events.append(event3)
    db.session.add_all([event1, event2, event3])
    db.session.commit()

    yield  # this is where the testing happens!


@pytest.fixture(scope='function')
def log_in_default_user(client):
    client.post('/login',
                json={'email': 'ronresnik79@gmail.com', 'password': 'SummerIsAwesome'})

    yield  # this is where the testing happens!


@pytest.fixture(scope='function')
def log_in_second_user(client):
    client.post('login',
                json={'email': 'ron@yahoo.com', 'password': 'SummerIsTheBest987'})

    yield   # this is where the testing happens!


@pytest.fixture
def valid_event_data():
    return {
        "title": "Valid Title",
        "description": "Valid Description",
        "venue": "Valid Venue",
        "event_date": datetime.now() + timedelta(days=1),
        "tags": [],
        "participants": None
    }


@pytest.fixture(scope='module')
def cli_test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    runner = flask_app.test_cli_runner()

    yield runner  # this is where the testing happens!
