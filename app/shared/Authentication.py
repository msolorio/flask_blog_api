import jwt, os, datetime
from flask import json, request, g
from functools import wraps
from ..models.User import User

class Auth():
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }

            token = jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            )

            return token

        except Exception as e:
            print('error:', e)

            return { 'error': 'error generating token' }, 400


    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), 'HS256')
            return { 'user_id': payload['sub'] }
        except jwt.ExpiredSignatureError as e:
            return { 'error': 'Token expired. Please login again.' }
        except jwt.InvalidTokenError as e:
            return { 'error': 'Token invalid. Try again with new token.' }


    @staticmethod
    def auth_required(func):
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return { 'error': 'Auth token not available. Please login' }, 401

            token = request.headers.get('api-token')

            data = Auth.decode_token(token)

            if data.get('error') or not data.get('user_id'):
                return data, 401

            user_id = data.get('user_id')
            user = User.get_one_user(user_id)

            if not user:
                return { 'error': 'user does not exist. Invalid token' }, 401

            # global data accessible across a single request
            g.user = { 'id': user_id }

            return func(*args, **kwargs)

        return decorated_auth