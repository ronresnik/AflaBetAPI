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
            location=data['location'],
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
def get_events():
    try:
        # Retrieve query parameters from the request
        location = request.args.get('location')
        venue = request.args.get('venue')
        sort_by = request.args.get('sort_by')

        # Check if sort_by is a valid option
        valid_sort_options = ['date', 'popularity', 'creation_time']
        if sort_by and sort_by not in valid_sort_options:
            raise ValueError(
                "Invalid value for sort_by. Must be one of 'date', 'popularity', 'creation_time'.")

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

        event_list = []
        for event in events:
            event_list.append({
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'venue': event.venue,
                'location': event.location,
                'event_date': event.event_date.strftime('%Y-%m-%d %H:%M:%S'),
                'tags': event.tags,
                'participants': event.participants,
            })
        return jsonify({'events': event_list})
    except ValueError as ve:
        return jsonify({'message': str(ve)}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500


# Endpoint to retrieve details of a specific event
@events_blueprint.route('/events/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    try:
        event = Event.query.get(event_id)
        if event:
            event_details = {
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'venue': event.venue,
                'location': event.location,
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
            user_events_ids = [event.id for event in user.events]
            if event_id not in user_events_ids:
                return jsonify({'message': "only owners of event can update it"}), 403
            data = request.get_json()
            event.description = data.get('description', event.description)
            event.venue = data.get('venue', event.venue)
            event.location = data.get('location', event.location)
            event.event_date = datetime.strptime(
                data.get('event_date', event.event_date), '%Y-%m-%d %H:%M:%S')
            event.tags = data.get('tags', event.tags)
            event.participants = data.get('participants', event.participants)
            db.session.commit()  # updates the user .events automatically
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
            user_events_ids = [event.id for event in user.events]
            if event_id not in user_events_ids:
                return jsonify({'message': "only owners of event can delete it"}), 403
            user.events.remove(event)
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
