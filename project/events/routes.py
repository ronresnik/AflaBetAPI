from datetime import datetime
from flask import (abort, current_app, render_template,
                   request, url_for, jsonify)
from pydantic import BaseModel, ValidationError, validator
from functools import wraps
import jwt
from sqlalchemy.exc import SQLAlchemyError
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
                id=data['public_id']).first()
        except Exception as e:
            return jsonify({'message': f'token is invalid, error: {str(e)}'})

        return f(current_user, *args, **kwargs)
    return decorator


@events_blueprint.route('/events', methods=['POST'])
@token_required
def schedule_event(user):
    try:
        data = request.get_json()
        new_event = Event(
            title=data['title'],
            description=data['description'],
            venue=data['venue'],
            event_date=datetime.strptime(
                data['event_date'], '%Y-%m-%d %H:%M:%S'),
            tags=data.get('tags', []),
        )
        user.events.append(new_event)
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Event scheduled successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# Endpoint to retrieve a list of all scheduled events


@events_blueprint.route('/events', methods=['GET'])
def get_all_events():
    """
    # Retrieve query parameters from the request
    location = request.args.get('location')
    venue = request.args.get('venue')
    sort_by = request.args.get('sort_by')

    # Construct the base query
    base_query = Event.query

    # Filter events based on location or venue
    if location:
        base_query = base_query.filter(Event.location == location)
    if venue:
        base_query = base_query.filter(Event.venue == venue)

    # Retrieve and sort events based on the specified parameter
    if sort_by == 'date':
        events = base_query.order_by(Event.event_date).all()
    elif sort_by == 'popularity':
        events = base_query.order_by(Event.participants.desc()).all()
    elif sort_by == 'creation_time':
        events = base_query.order_by(Event.created_at).all()
    else:
        events = base_query.all()

    """
    try:
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
            })
        return jsonify({'events': event_list})
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Endpoint to retrieve details of a specific event
@events_blueprint.route('/events/<int:event_id>', methods=['GET'])
@token_required
def get_event_details(user, event_id):
    try:
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
            }
            return jsonify(event_details)
        else:
            return jsonify({'message': 'Event not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Endpoint to update details of a specific event
@events_blueprint.route('/events/<int:event_id>', methods=['PUT'])
@token_required
def update_event(user, event_id):
    try:
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
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 400


# Endpoint to delete a specific event
@events_blueprint.route('/events/<int:event_id>', methods=['DELETE'])
@token_required
def delete_event(user, event_id):
    try:
        event = Event.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return jsonify({'message': 'Event deleted successfully'})
        else:
            return jsonify({'message': 'Event not found'}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
    except Exception as e:
        return jsonify({'message': str(e)}), 400
