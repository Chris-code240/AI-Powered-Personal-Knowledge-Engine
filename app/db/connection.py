import psycopg2
from contextlib import contextmanager
import dotenv
import os
dotenv.load_dotenv()

@contextmanager
def connection(dbname = os.getenv("DB_NAME"), 
               user = os.getenv("DB_USER"), 
               password = os.getenv("DB_PASSWORD"), 
               host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT")):
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = conn.cursor()
        yield conn, cursor
        conn.commit()  # commit if all went well
    except Exception as e:
        if conn:
            conn.rollback()  # rollback on error
        raise e
    finally:
        if conn:
            cursor.close()
            conn.close()
