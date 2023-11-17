import json
from datetime import datetime
from project.models import Event
from project.events.routes import get_events


def test_get_events_with_location(client, init_database):
    # Create test events
    event1 = Event(
        title='Test Event 1',
        description='This is a test event 1',
        venue='Test Venue 1',
        location='Test Location 1',
        event_date=datetime(2022, 1, 1, 12, 0, 0),
        tags=['test', 'event']
    )
    event2 = Event(
        title='Test Event 2',
        description='This is a test event 2',
        venue='Test Venue 2',
        location='Test Location 2',
        event_date=datetime(2022, 1, 2, 12, 0, 0),
        tags=['test', 'event']
    )
    event3 = Event(
        title='Test Event 3',
        description='This is a test event 3',
        venue='Test Venue 3',
        location='Test Location 1',
        event_date=datetime(2022, 1, 3, 12, 0, 0),
        tags=['test', 'event']
    )
    init_database([event1, event2, event3])

    # Make request to get events with location 'Test Location 1'
    response = client.get('/events?location=Test%20Location%201')

    # Check that the response is successful
    assert response.status_code == 200

    # Check that the response contains the correct events
    expected_response = {
        'events': [
            {
                'id': event1.id,
                'title': 'Test Event 1',
                'description': 'This is a test event 1',
                'venue': 'Test Venue 1',
                'location': 'Test Location 1',
                'event_date': '2022-01-01 12:00:00',
                'tags': ['test', 'event'],
                'participants': 0
            },
            {
                'id': event3.id,
                'title': 'Test Event 3',
                'description': 'This is a test event 3',
                'venue': 'Test Venue 3',
                'location': 'Test Location 1',
                'event_date': '2022-01-03 12:00:00',
                'tags': ['test', 'event'],
                'participants': 0
            }
        ]
    }
    assert json.loads(response.data) == expected_response


def test_get_events_with_venue(client, init_database):
    # Create test events
    event1 = Event(
        title='Test Event 1',
        description='This is a test event 1',
        venue='Test Venue 1',
        location='Test Location 1',
        event_date=datetime(2022, 1, 1, 12, 0, 0),
        tags=['test', 'event']
    )
    event2 = Event(
        title='Test Event 2',
        description='This is a test event 2',
        venue='Test Venue 2',
        location='Test Location 2',
        event_date=datetime(2022, 1, 2, 12, 0, 0),
        tags=['test', 'event']
    )
    event3 = Event(
        title='Test Event 3',
        description='This is a test event 3',
        venue='Test Venue 1',
        location='Test Location 3',
        event_date=datetime(2022, 1, 3, 12, 0, 0),
        tags=['test', 'event']
    )
    init_database([event1, event2, event3])

    # Make request to get events with venue 'Test Venue 1'
    response = client.get('/events?venue=Test%20Venue%201')

    # Check that the response is successful
    assert response.status_code == 200

    # Check that the response contains the correct events
    expected_response = {
        'events': [
            {
                'id': event1.id,
                'title': 'Test Event 1',
                'description': 'This is a test event 1',
                'venue': 'Test Venue 1',
                'location': 'Test Location 1',
                'event_date': '2022-01-01 12:00:00',
                'tags': ['test', 'event'],
                'participants': 0
            },
            {
                'id': event3.id,
                'title': 'Test Event 3',
                'description': 'This is a test event 3',
                'venue': 'Test Venue 1',
                'location': 'Test Location 3',
                'event_date': '2022-01-03 12:00:00',
                'tags': ['test', 'event'],
                'participants': 0
            }
        ]
    }
    assert json.loads(response.data) == expected_response


def test_get_events_with_sort_by(client, init_database):
    # Create test events
    event1 = Event(
        title='Test Event 1',
        description='This is a test event 1',
        venue='Test Venue 1',
        location='Test Location 1',
        event_date=datetime(2022, 1, 1, 12, 0, 0),
        tags=['test', 'event'],
        participants=10
    )
    event2 = Event(
        title='Test Event 2',
        description='This is a test event 2',
        venue='Test Venue 2',
        location='Test Location 2',
        event_date=datetime(2022, 1, 2, 12, 0, 0),
        tags=['test', 'event'],
        participants=5
    )
    event3 = Event(
        title='Test Event 3',
        description='This is a test event 3',
        venue='Test Venue 3',
        location='Test Location 3',
        event_date=datetime(2022, 1, 3, 12, 0, 0),
        tags=['test', 'event'],
        created_at=datetime(2022, 1, 1, 12, 0, 0)
    )
    init_database([event1, event2, event3])

    # Make request to get events sorted by popularity
    response = client.get('/events?sort_by=popularity')

    # Check that the response is successful
    assert response.status_code == 200

    # Check that the response contains the correct events
    expected_response = {
        'events': [
            {
                'id': event1.id,
                'title': 'Test Event 1',
                'description': 'This is a test event 1',
                'venue': 'Test Venue 1',
                'location': 'Test Location 1',
                'event_date': '2022-01-01 12:00:00',
                'tags': ['test', 'event'],
                'participants': 10
            },
            {
                'id': event2.id,
                'title': 'Test Event 2',
                'description': 'This is a test event 2',
                'venue': 'Test Venue 2',
                'location': 'Test Location 2',
                'event_date': '2022-01-02 12:00:00',
                'tags': ['test', 'event'],
                'participants': 5
            },
            {
                'id': event3.id,
                'title': 'Test Event 3',
                'description': 'This is a test event 3',
                'venue': 'Test Venue 3',
                'location': 'Test Location 3',
                'event_date': '2022-01-03 12:00:00',
                'tags': ['test', 'event'],
                'participants': 0
            }
        ]
    }
    assert json.loads(response.data) == expected_response


def test_get_events_with_invalid_sort_by(client, init_database):
    # Make request to get events with invalid sort_by parameter
    response = client.get('/events?sort_by=invalid')

    # Check that the response is unsuccessful
    assert response.status_code == 400

    # Check that the response contains the correct error message
    expected_response = {
        'message': "Invalid value for sort_by. Must be one of 'date', 'popularity', 'creation_time'."}
    assert json.loads(response.data) == expected_response
