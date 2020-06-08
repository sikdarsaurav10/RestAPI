import os


class Config:

    SECRET_KEY = os.urandom(16)
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////mnt/e/flask_API/zenithApp/webApp/Data.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
