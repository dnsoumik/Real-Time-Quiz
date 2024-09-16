
import sys
import datetime as dtime
import jwt
import random
from bson.objectid import ObjectId
from utils.log_util import Log

# Append the utils path for custom modules
sys.path.append('./utils')

# List of secret keys for JWT encoding and decoding
SECRET = 'IS-*HGJHFKJLLKJHLKJHlko87o876ljkLIGHO'

# JWT options for decoding and validation
OPTIONS = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}

import jwt
import datetime
import tornado.web

# External class for handling JWT
class JWTHandler:
    def __init__(self):
        self.algorithm = 'HS256'
        self.exp_seconds = 3600

    def generate_token(self, user_id):
        """Generates JWT token for a given user ID"""

        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=self.exp_seconds)
        }
        token = jwt.encode(payload, SECRET, algorithm=self.algorithm)
        return token

    def decode_token(self, token):
        """Validates and decodes the JWT token"""
        try:
            decoded_token = jwt.decode(token, SECRET, algorithms=[self.algorithm])
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise tornado.web.HTTPError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise tornado.web.HTTPError(401, "Invalid token")
