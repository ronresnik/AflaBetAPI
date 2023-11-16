"""
The Event Blueprint handles the scheduling, Retrivition, Updtaing and deletion of events for the users of this API.
"""
from flask import Blueprint


events_blueprint = Blueprint('events', __name__)

from . import routes  # nopep8
