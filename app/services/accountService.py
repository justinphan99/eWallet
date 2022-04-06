from cgitb import handler
import uuid
import psycopg2
from app.response.badRequestHandler import BadRequestHandler
from app.utils.baseFunc import encode_auth_token,decode_auth_token

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

def create_accountType():
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""CREATE TYPE accountType AS ENUM ('merchant', 'personal', 'issuer');""")
        conn.commit()
        cur.close()
        print(">>> Create enum accountType successfully")
    except Exception as e:
        print(">>> Cannot create enum accountType")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            conn.close()

def create_table_account():
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.account
            (
                accountId UUID PRIMARY KEY,
                accountType accountType,
                balance FLOAT DEFAULT 0,
                merchantId UUID REFERENCES merchant(merchantId)
            ); 
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        print("Error: " +str(e))
    finally:
        if conn is not None:
            conn.close()

def select_all_account():
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM public.account;
        """)
        data = cur.fetchall()
        print(data)
        print(">>> Select * from table account successfully")
        return data
    except Exception as e:
        print(">>> Cannot select * from table account")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def select_an_account(account_id,conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.account WHERE account.accountId = '{}'""".format(account_id))
        data = cur.fetchone()
        if data == ():
            return data
        else:
            accountType = data[1]
            accountId = data[0]
            balance = data[2]
            data_dict = {
                "accountType": accountType,
                "accountId": accountId,
                "balance": balance
            }
            data = data_dict
            return data
    except Exception as e:
        print(">>> Cannot select an account from table account")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def create_an_account(data):
    accountType = str(data['accountType'])

    if accountType == 'personal' or accountType == 'issuer':
        conn = connection()
        try:
            cur = conn.cursor()
            accountId = str(uuid.uuid4())
            cur.execute("""INSERT INTO public.account (accountId, accountType)
            VALUES ('{0}','{1}')""".format(accountId,accountType))
            conn.commit()    
            data = select_an_account(accountId,conn) 
            return data
        except Exception as e:
            print(">>> Cannot create account")
            print("Error: " +str(e))
        finally:
            if conn is not None:
                cur.close()
                conn.close()
    else:
        handler = BadRequestHandler()
        return handler

def create_a_merchant_account(accountId, merchantId):
    conn = connection()
    try:
        accountType = 'merchant'
        cur = conn.cursor()
        cur.execute("""INSERT INTO public.account (accountId, accountType, merchantId)
        VALUES ('{0}','{1}','{2}')""".format(accountId,accountType,merchantId))
        conn.commit()    
        cur.close()
        print("create a merchant account")
        return
    except Exception as e:
        print(">>> Cannot create account")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def get_account_token(accountId):
    conn = connection()
    data = select_an_account(accountId,conn)
    if data == ():
        handler = BadRequestHandler()
        return handler
    else:
        data = encode_auth_token(accountId)
        return data