import jwt
from app.utils.config import key
import datetime
import psycopg2

def connection():
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="eWallet",
        user="admin",
        password="admin")
    except Exception as e:
        print(">>> Cannot connect to Database")
        print("Error: " + str(e))
    return conn


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

