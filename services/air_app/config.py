"""Flask app config module"""
import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env.dev"))


class Config:
    """app config object"""

    FLASK_APP = os.environ.get("FLASK_APP")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRES_AIR_QUALITY_USER = os.environ.get("POSTGRES_AIR_QUALITY_USER")
    POSTGRES_AIR_QUALITY_USER_PW = os.environ.get("POSTGRES_AIR_QUALITY_USER_PW")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")
