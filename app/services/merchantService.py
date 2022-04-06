import uuid
import psycopg2
from app.services.accountService import create_a_merchant_account


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

def create_table_merchant():
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS public.merchant
            (
                merchantName VARCHAR(200),
                merchantId UUID PRIMARY KEY,
                apiKey UUID,
                merchantUrl VARCHAR(200) DEFAULT 'http://localhost:8080'
            ); 
        """)
        conn.commit()
        print(">>> Create table merchant successfully")
    except Exception as e:
        print(">>> Cannot create table merchant")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def select_all_account():
    conn = connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM public.merchant;
        """)
        data = cur.fetchall()
        print(data)
        print(">>> Select * from table merchant successfully")
        return data
    except Exception as e:
        print(">>> Cannot select * from table merchant")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def select_a_merchant(merchantId, accountId, conn):
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * FROM public.merchant WHERE merchant.merchantId = '{0}'
        """.format(merchantId))
        data = cur.fetchone()
        merchantName = data[0]
        accountId = accountId
        merchantId = data[1]
        apiKey = data[2]
        merchantUrl = data[3]
        data_dict = {
            "merchantName": merchantName,
            "accountId": accountId,
            "merchantId": merchantId,
            "apiKey": apiKey,
            "merchantUrl": merchantUrl
        }
        data = data_dict
        print("select a merchant")
        return data
    except Exception as e:
        print(">>> Cannot select an merchant from table merchant")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def create_a_merchant(data):
    conn = connection()
    try:
        cur = conn.cursor()
        merchantName = str(data['merchantName'])
        accountId = str(uuid.uuid4())
        merchantId = str(uuid.uuid4())
        apiKey = str(uuid.uuid4())
        merchantUrl = str(data['merchantUrl'])

        cur.execute("""INSERT INTO public.merchant (merchantName,merchantId,apiKey,merchantUrl)
        VALUES ('{0}','{1}', '{2}', '{3}')
        """.format(merchantName,merchantId,apiKey,merchantUrl))
        conn.commit()  
        cur.close()  
        print("create a merchant")
        create_a_merchant_account(accountId,merchantId)
        data = select_a_merchant(merchantId, accountId, conn) 
        return data
    except Exception as e:
        print(">>> Cannot create merchant")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()
