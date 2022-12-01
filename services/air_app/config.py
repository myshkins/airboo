"""Flask app config module"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env.dev"))

class Config():
    """app config object"""
    FLASK_APP = os.environ.get("FLASK_APP")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

