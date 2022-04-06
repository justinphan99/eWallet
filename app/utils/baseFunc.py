import jwt
from app.utils.config import key
import datetime

def encode_auth_token(accountId: str):
        try:
            payload = {
                'sub': accountId
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, key, algorithms=["HS256"])
            return payload['sub']
        except Exception as e:
            print("error : " + str(e))