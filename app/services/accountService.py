import uuid
import psycopg2

def connection():
    try:
        conn = psycopg2.connect(
        host="localhost",
        database="eWallet",
        user="admin",
        password="admin")
        print(">>> Connect to Database succesfull")
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
                accountId UUID primary key,
                accountType accountType,
                balance float
            ); 
        """)
        conn.commit()
        cur.close()
        print(">>> Create table account successfully")
    except Exception as e:
        print(">>> Cannot create table account")
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
        print(">>> Cannot select * from table account account")
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

def create_a_account(data):
    conn = connection()
    try:
        cur = conn.cursor()
        account_id = str(uuid.uuid4())
        cur.execute("""INSERT INTO public.account VALUES ('{0}','{1}')""".format(account_id,data))
        conn.commit()    
        data = select_an_account(account_id,conn) 
        return data
    except Exception as e:
        print(">>> Cannot create account")
        print("Error: " +str(e))
    finally:
        if conn is not None:
            cur.close()
            conn.close()
