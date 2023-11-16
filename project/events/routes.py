from datetime import datetime
from flask import (abort, current_app, render_template,
                   request, url_for, jsonify)
from pydantic import BaseModel, ValidationError, validator
from functools import wraps
import jwt

from project import db
from project.models import Event, User
from config import settings

from . import events_blueprint


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(
                token, settings.JWT_HS256_SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(
                public_id=data['public_id']).first()
        except Exception as e:
            return jsonify({'message': f'token is invalid, error: {str(e)}'})

        return f(current_user, *args, **kwargs)
    return decorator


@events_blueprint.route('/events', methods=['POST'])
def schedule_event():
    data = request.get_json()
    new_event = Event(
        title=data['title'],
        description=data['description'],
        venue=data['venue'],
        event_date=datetime.strptime(data['event_date'], '%Y-%m-%d %H:%M:%S'),
        tags=data.get('tags', []),
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'message': 'Event scheduled successfully'}), 201

# Endpoint to retrieve a list of all scheduled events


@events_blueprint.route('/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    event_list = []
    for event in events:
        event_list.append({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'venue': event.venue,
            'event_date': event.event_date.strftime('%Y-%m-%d %H:%M:%S'),
            'tags': event.tags,
            'participants': event.participants,
            'subscribers': event.subscribers,
        })
    return jsonify({'events': event_list})

# Endpoint to retrieve details of a specific event


@events_blueprint.route('/events/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    event = Event.query.get(event_id)
    if event:
        event_details = {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'venue': event.venue,
            'event_date': event.event_date.strftime('%Y-%m-%d %H:%M:%S'),
            'tags': event.tags,
            'participants': event.participants,
            'subscribers': event.subscribers,
        }
        return jsonify(event_details)
    else:
        return jsonify({'message': 'Event not found'}), 404

# Endpoint to update details of a specific event


@events_blueprint.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.get(event_id)
    if event:
        data = request.get_json()
        event.title = data['title']
        event.description = data['description']
        event.venue = data['venue']
        event.event_date = datetime.strptime(
            data['event_date'], '%Y-%m-%d %H:%M:%S')
        event.tags = data.get('tags', [])
        db.session.commit()
        return jsonify({'message': 'Event updated successfully'})
    else:
        return jsonify({'message': 'Event not found'}), 404

# Endpoint to delete a specific event


@events_blueprint.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Event deleted successfully'})
    else:
        return jsonify({'message': 'Event not found'}), 404
