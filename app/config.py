# TODO: UPDATE TO PULL FROM ENV VARS
import os

# DEBUG = True
DEBUG = os.getenv('DEBUG')

# SQLALCHEMY_DATABASE_URI = 'postgresql://michael@localhost:5432/flask_blog_db'
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

# JWT_SECRET_KEY = 'thisisasecret'
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

SQLALCHEMY_TRACK_MODIFICATIONS = False
