import imp
import psycopg2
import uuid
from app.utils.baseFunc import decode_auth_token
import hashlib
import json
from app.services.accountService import *

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
        cur.execute("""CREATE TYPE transactionStatus AS ENUM ('initialized', 'confirmed', 'verified', 'canceled', 'expired', 'failed');""")
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
            CREATE TABLE IF NOT EXISTS public.Transaction(
                transactionId UUID PRIMARY KEY,
                transactionStatus transactionStatus,
                incomeAccount UUID,
                outcomeAccount UUID,
                amount FLOAT DEFAULT 0,
                extraData VARCHAR(200),
                signature UUID,
                merchantId UUID REFERENCES merchant(merchantId),
                createdAt timestamp without time zone DEFAULT CURRENT_TIMESTAMP
                );
        """)
        conn.commit()
        cur.close()
    except Exception as e:
        print("Error: " +str(e))
    finally:
        if conn is not None:
            conn.close()

def create_a_transaction(data, token):
    conn = connection()
    accountMerchantId = decode_auth_token(token)
    accountType = select_an_account(accountMerchantId,conn)["accountType"]
    if str(accountType) == 'merchant':
        transactionId = str(uuid.uuid4())
        merchantId = data['merchantId']
        incomeAccount = decode_auth_token(token)
        outcomeAccount = ''
        amount = data['amount']
        extraData = data['extraData']
        dataTemp = {"merchantId": merchantId, "amount": amount, "extraData": extraData}
        signature = hashlib.md5(json.dumps(dataTemp).encode('utf-8')).hexdigest()
        status = 'INITIALIZED'
        try:
            query = """INSERT INTO public.transaction 
            (transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            VALUES ('{0}','{1}', '{2}', {3}, '{4}', '{5}', '{6}');""".format(transactionId, merchantId, incomeAccount, amount, extraData, signature, status)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()    
            print("create a transaction")
            data = select_a_transaction(transactionId, conn)
            return data
        
        except Exception as e:
            print(">>> Cannot create transaction")
            print("Error: " +str(e))
        finally:
            if conn is not None:
                cur.close()
                conn.close()
    else:
        return "403"


def select_a_transaction(transactionId,conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.transaction WHERE transaction.transactionId = '{}'""".format(transactionId))
        data = cur.fetchone()
        if data == ():
            return data
        else:
            transactionId = data[0]
            merchantId = data[1]
            incomeAccount = data[2]
            outcomeAccount = data[3]
            amount = data[4]
            extraData = data[5]
            signature = data[6]
            status = data[7]
            data_dict = {
                "transactionId": transactionId,
                "merchantId": merchantId,
                "incomeAccount": incomeAccount,
                "outcomeAccount": outcomeAccount,
                "amount": amount,
                "extraData": extraData,
                "signature": signature,
                "status": status
            }
            data = data_dict
            return data
    except Exception as e:
        print(">>> Cannot select an transaction from table transaction")
        print("Error: " +str(e))

def confirm_a_transaction(data, token):
    conn = connection()
    accountPersonalId = decode_auth_token(token)
    accountType = select_an_account(accountPersonalId,conn)["accountType"]
    transactionId = data['transactionId']
    if str(accountType) == 'personal':
        balance_account = float(get_balance_account(accountPersonalId))
        amount_transaction = float(get_amount_transaction(transactionId))
        if balance_account>0 and balance_account>=amount_transaction:
            status = 'CONFIRMED'
        else:
            status = 'FAILED'
        try:
            query = """UPDATE public.transaction SET status = '{0}'
            WHERE transaction.transactionId = '{1}'""".format(status, transactionId)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()    
            print("confirm a transaction")
            data = {
                "code": "SUC",
                "message": "transaction {}".format(status)
            }
            return data
        
        except Exception as e:
            print(">>> Cannot update transaction")
            print("Error: " +str(e))
        finally:
            if conn is not None:
                cur.close()
                conn.close()
    else:
        return "403"


def get_amount_transaction(transactionId):
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""SELECT amount FROM public.transaction WHERE transaction.transactionId = '{}'""".format(transactionId))
        data = cur.fetchone()
        return data[0]
    except Exception as e:
        print(">>> Cannot select an transaction from table transaction")
        print("Error: " +str(e))


def verify_a_transaction(data, token):
    conn = connection()
    accountPersonalId = decode_auth_token(token)
    accountType = select_an_account(accountPersonalId,conn)["accountType"]
    transactionId = data['transactionId']
    if str(accountType) == 'personal':
        balance_account = float(get_balance_account(accountPersonalId))
        amount_transaction = float(get_amount_transaction(transactionId))
        if balance_account>0 and balance_account>=amount_transaction:
            status = 'VERIFIED'
            balance_account = balance_account - amount_transaction
        else:
            status = 'FAILED'
        try:
            query = """UPDATE public.transaction SET status = '{0}', outcomeAccount = '{1}'
            WHERE transaction.transactionId = '{2}'""".format(status, accountPersonalId, transactionId)
            print(query)
            cur = conn.cursor()
            cur.execute(query)

            query = """UPDATE public.account SET balance = {0}
            WHERE account.accountId = '{1}'""".format(balance_account, accountPersonalId)
            print(query)
            cur.execute(query)
            conn.commit()

            print("verify a transaction")

            data = {
                "code": "200",
                "message": "transaction {}".format(status)
            }
            return data
        
        except Exception as e:
            print(">>> Cannot update transaction")
            print("Error: " +str(e))
        finally:
            if conn is not None:
                cur.close()
                conn.close()
    else:
        return "403"


def cancel_a_transaction(data, token):
    conn = connection()
    accountPersonalId = decode_auth_token(token)
    accountType = select_an_account(accountPersonalId,conn)["accountType"]
    transactionId = data['transactionId']
    if str(accountType) == 'personal':
        status = 'CANCELED'
        try:
            query = """UPDATE public.transaction SET status = '{0}'
            WHERE transaction.transactionId = '{1}'""".format(status, transactionId)
            print(query)
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()

            print("cancel a transaction")

            data = {
                "code": "200",
                "message": "transaction {}".format(status)
            }
            return data
        
        except Exception as e:
            print(">>> Cannot cancel transaction")
            print("Error: " +str(e))
        finally:
            if conn is not None:
                cur.close()
                conn.close()
    else:
        return "403"