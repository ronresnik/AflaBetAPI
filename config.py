import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    DATABASE_URI_SCHEME: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    ACCESS_TOKEN_EXPIRES_IN: str
    REFRESH_TOKEN_EXPIRES_IN: int
    JWT_ALGORITHM: str

    JWT_HS256_SECRET_KEY: str
    FLASK_APP: str

    class Config:
        env_file = './.env'


settings = Settings()
SQLALCHEMY_DATABASE_URL = f"{settings.DATABASE_URI_SCHEME}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/"
# Determine the folder of the top-level directory of this project
BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False
    SECRET_KEY = settings.JWT_HS256_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Logging
    LOG_WITH_GUNICORN = True  # os.getenv('LOG_WITH_GUNICORN', default=False)
    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"


class ProductionConfig(Config):
    FLASK_ENV = 'production'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
