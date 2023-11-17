import json
from unittest.mock import patch
from project.models import User


def test_register_new_user(client, db):
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        mock_request.get_json.return_value = {
            'email': 'test@example.com', 'password': 'Abcd1234!'}
        response = client.post('/register')
        assert response.status_code == 200
        assert json.loads(response.data) == {
            'message': 'registered successfully'}
        assert db.session.query(User).filter_by(
            email='test@example.com').count() == 1


def test_register_existing_user(client, db):
    user = User('test@example.com', 'Abcd1234!')
    db.session.add(user)
    db.session.commit()
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        mock_request.get_json.return_value = {
            'email': 'test@example.com', 'password': 'Abcd1234!'}
        response = client.post('/register')
        assert response.status_code == 200
        assert json.loads(response.data) == {
            'message': f'ERROR! Email ({user.email}) already exists in the database.'}
        assert db.session.query(User).filter_by(
            email='test@example.com').count() == 1


def test_register_invalid_email(client, db):
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        mock_request.get_json.return_value = {
            'email': 'invalid_email', 'password': 'Abcd1234!'}
        response = client.post('/register')
        assert response.status_code == 504
        assert response.headers['Authentication'] == 'register failed"'
        assert db.session.query(User).filter_by(
            email='invalid_email').count() == 0


def test_register_invalid_password(client, db):
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        mock_request.get_json.return_value = {
            'email': 'test@example.com', 'password': 'invalid_password'}
        response = client.post('/register')
        assert response.status_code == 504
        assert response.headers['Authentication'] == 'register failed"'
        assert db.session.query(User).filter_by(
            email='test@example.com').count() == 0


def test_login_success(client, db):
    user = User('test@example.com', 'Abcd1234!')
    db.session.add(user)
    db.session.commit()
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        mock_request.authorization = ('test@example.com', 'Abcd1234!')
        response = client.post('/login')
        assert response.status_code == 200
        assert 'token' in json.loads(response.data)


def test_login_missing_credentials(client, db):
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        response = client.post('/login')
        assert response.status_code == 401
        assert response.headers['Authentication'] == 'login required"'


def test_login_invalid_credentials(client, db):
    user = User('test@example.com', 'Abcd1234!')
    db.session.add(user)
    db.session.commit()
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        mock_request.authorization = ('test@example.com', 'invalid_password')
        response = client.post('/login')
        assert response.status_code == 401
        assert response.headers['Authentication'] == 'login required"'


def test_login_nonexistent_user(client, db):
    with patch('flask.request') as mock_request:
        mock_request.method = 'POST'
        mock_request.authorization = ('nonexistent@example.com', 'Abcd1234!')
        response = client.post('/login')
        assert response.status_code == 401
        assert response.headers['Authentication'] == 'login required"'
