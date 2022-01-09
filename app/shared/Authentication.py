import jwt, os, datetime
from flask import json, request, g
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
