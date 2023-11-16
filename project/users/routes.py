from datetime import datetime, timedelta
import os
import jwt

import sqlalchemy as sa
from flask import (current_app, render_template, request,
                   url_for, make_response, jsonify)
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError
from config import settings

from project import db
from project.models import User

from . import users_blueprint


@users_blueprint.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
            new_user = User(data['email'], data['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'registered successfully'})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'message': f'ERROR! Email ({new_user.email}) already exists in the database.'})
    return make_response("error", 504, {'Authentication': 'register failed"'})


@users_blueprint.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'Authentication': 'login required"'})
        email = auth.username
        user = User.query.filter_by(email=email).first()
        if user and user.is_password_correct(auth.password):
            token = jwt.encode({'public_id': user.id, 'exp': datetime.utcnow(
            ) + timedelta(minutes=45)}, settings.JWT_HS256_SECRET_KEY, "HS256")

            return jsonify({'token': token})

    return make_response('could not verify',  401, {'Authentication': '"login required"'})
