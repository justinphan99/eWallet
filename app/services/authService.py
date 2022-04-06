from ..utils.baseFunc import decode_auth_token
import app.services.accountService as AccountService
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

def getLoggedInAccount(authToken):
    if (authToken):
        resp = decode_auth_token(authToken)
        conn = connection()
        account = AccountService.select_an_account(resp, conn)
        if account:
            return account
        return account
    return account