import psycopg2
from contextlib import contextmanager
import dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


dotenv.load_dotenv()
from ..config.config import load_settings

settings = load_settings()

db_uri = (
    settings["database"]["uri"] or
    f"postgresql://{settings['database']['user']}:{settings['database']['password']}@"
    f"{settings['database']['host']}:{settings['database']['port']}/{settings['database']['name']}"
)


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


engine = create_engine(db_uri)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@contextmanager
def session_connection():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise
    finally:
        session.close()

