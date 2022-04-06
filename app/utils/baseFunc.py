import jwt
from app.utils.config import key
import datetime

def encode_auth_token(accountId: str):
        try:
            payload = {
                'exp': datetime.datetime.utcnow(),
                'iat': datetime.datetime.utcnow(),
                'sub': accountId
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

def decode_auth_token(auth_token: str):
        try:
            payload = jwt.decode(auth_token, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'