import pytest
from sqlalchemy.exc import IntegrityError
from project import db
from project.models import Event

from datetime import datetime, timedelta


def test_valid_event_creation(valid_event_data):
    event = Event(**valid_event_data)
    assert event.title == valid_event_data["title"]
    assert event.description == valid_event_data["description"]
    assert event.venue == valid_event_data["venue"]
    assert event.event_date == valid_event_data["event_date"]
    assert event.tags == valid_event_data["tags"]
    assert event.participants == valid_event_data["participants"]


def test_empty_title():
    with pytest.raises(ValueError, match="Title must be non-empty and between 5 and 255 characters long."):
        Event("", "Valid Description", "Valid Venue",
              datetime.now() + timedelta(days=1), [], None)


def test_short_title():
    with pytest.raises(ValueError, match="Title must be non-empty and between 5 and 255 characters long."):
        Event("Short", "Valid Description", "Valid Venue",
              datetime.now() + timedelta(days=1), [], None)


def test_long_title():
    with pytest.raises(ValueError, match="Title must be non-empty and between 5 and 255 characters long."):
        Event("Too long title" * 30, "Valid Description", "Valid Venue",
              datetime.now() + timedelta(days=1), [], None)


def test_empty_description():
    with pytest.raises(ValueError, match="Description must be non-empty and between 5 and 255 characters long."):
        Event("Valid Title", "", "Valid Venue",
              datetime.now() + timedelta(days=1), [], None)


def test_short_description():
    with pytest.raises(ValueError, match="Description must be non-empty and between 5 and 255 characters long."):
        Event("Valid Title", "Short", "Valid Venue",
              datetime.now() + timedelta(days=1), [], None)


def test_long_description():
    with pytest.raises(ValueError, match="Description must be non-empty and between 5 and 255 characters long."):
        Event("Valid Title", "Too long description" * 30, "Valid Venue",
              datetime.now() + timedelta(days=1), [], None)


def test_empty_venue():
    with pytest.raises(ValueError, match="Venue must be non-empty and between 5 and 255 characters long."):
        Event("Valid Title", "Valid Description", "",
              datetime.now() + timedelta(days=1), [], None)


def test_short_venue():
    with pytest.raises(ValueError, match="Venue must be non-empty and between 5 and 255 characters long."):
        Event("Valid Title", "Valid Description", "Short",
              datetime.now() + timedelta(days=1), [], None)


def test_long_venue():
    with pytest.raises(ValueError, match="Venue must be non-empty and between 5 and 255 characters long."):
        Event("Valid Title", "Valid Description", "Too long venue" *
              30, datetime.now() + timedelta(days=1), [], None)


def test_empty_tags():
    event = Event("Valid Title", "Valid Description", "Valid Venue",
                  datetime.now() + timedelta(days=1), None, None)
    assert event.tags == []


def test_default_participants():
    event = Event("Valid Title", "Valid Description", "Valid Venue",
                  datetime.now() + timedelta(days=1), [], None)
    assert event.participants == 1


def test_negative_participants():
    with pytest.raises(ValueError, match="Participants must be greater than or equal to 1."):
        Event("Valid Title", "Valid Description", "Valid Venue",
              datetime.now() + timedelta(days=1), [], -1)


def test_event_date_in_past():
    with pytest.raises(ValueError, match="Event date cannot be in the past."):
        Event("Valid Title", "Valid Description", "Valid Venue",
              datetime.now() - timedelta(days=1), [], None)


def test_negative_participants():
    with pytest.raises(ValueError, match="Participants must be greater than or equal to 1."):
        Event("Valid Title", "Valid Description", "Valid Venue",
              datetime.now() + timedelta(days=1), [], -1)
