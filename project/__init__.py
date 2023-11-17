from datetime import timedelta
import logging
import os
from logging.handlers import RotatingFileHandler

import sqlalchemy as sa
from click import echo
from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
# -------------
# Configuration
# -------------

# Create the instances of the Flask extensions (flask-sqlalchemy, flask-login, etc.) in
# the global scope, but without any arguments passed in.  These instances are not attached
# to the application at this point.
db = SQLAlchemy()
mail = Mail()
# Initialize the scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.start()
# ----------------------------
# Application Factory Function
# ----------------------------


def create_app():
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_blueprints(app)
    configure_logging(app)
    register_cli_commands(app)
    configure_event_reminders(app)

    # Check if the database needs to be initialized
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table("users"):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info('Initialized the database!')
    else:
        app.logger.info('Database already contains the users table.')

    return app


# ----------------
# Helper Functions
# ----------------

def initialize_extensions(app):
    # Since the application instance is now created, pass it to each Flask
    # extension instance to bind it to the Flask application instance (app)
    db.init_app(app)

    # Flask-Login configuration
    from project.models import User


def register_blueprints(app):
    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    from project.users import users_blueprint
    from project.events import events_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(events_blueprint)

    swagger_ui_blueprint = get_swaggerui_blueprint(
        app.config['SWAGGER_URL'],
        app.config['API_URL'],
        config={
            'app_name': 'Access API'
        }
    )
    app.register_blueprint(swagger_ui_blueprint,
                           url_prefix=app.config['SWAGGER_URL'])


def configure_logging(app):
    # Logging Configuration
    if app.config['LOG_WITH_GUNICORN']:
        gunicorn_error_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers.extend(gunicorn_error_logger.handlers)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler = RotatingFileHandler('instance/flask-user-management.log',
                                           maxBytes=16384,
                                           backupCount=20)
        file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(threadName)s-%(thread)d: %(message)s [in %(filename)s:%(lineno)d]')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Remove the default logger configured by Flask
    app.logger.removeHandler(default_handler)

    app.logger.info('Starting the Flask User Management App...')


def configure_event_reminders(app):
    # i will not actually send emails
    app.config['MAIL_SERVER'] = 'mail_server'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'your_username'
    app.config['MAIL_PASSWORD'] = 'your_password'
    app.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'
    mail.init_app(app)


def register_cli_commands(app):
    @app.cli.command('init_db')
    def initialize_database():
        """Initialize the database."""
        db.drop_all()
        db.create_all()
        echo('Initialized the database!')


# Define a function to send reminders
def send_reminder(event, user_email):
    # Print the reminder to the console
    print(
        f"Reminder: User: {user_email} Your event '{event.title}' is scheduled in 30 minutes!")

    # Send reminder via email Code - do not Actually send
    """
    msg = Message('Event Reminder', recipients=[user_email])
    msg.body = f"Hello {user_email},\n\nThis is a reminder that your event '{event.title}' is scheduled in 30 minutes!\n\nBest regards,\nYour Event App"
    mail.send(msg)
    """

# Function to schedule an event and reminder


def schedule_event_with_reminder(event, user_email):
    # Schedule the event
    scheduler.add_job(func=send_reminder, trigger='date',
                      run_date=event.event_date - timedelta(minutes=30), args=[event, user_email])

    # Save the event to the database or perform any other necessary operations
