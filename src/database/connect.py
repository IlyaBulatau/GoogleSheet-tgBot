import psycopg2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

from config import config

from logger.logger import logger

def create_database():
    """
    Создание таблицы БД
    """
    connect = psycopg2.connect(
        database='postgres',
        user=config.DB_LOGIN,
        password=config.DB_PASSWORD,
        host=config.DB_HOST
    )
    connect.autocommit = True

    cursor = connect.cursor()
    
    try:
        sql_query = f'CREATE DATABASE {config.DB_NAME}'
        cursor.execute(sql_query)
        logger.warning('CREATE DATABASE')
    except:
        ...
    connect.close()

# создание соединения с базой данных
engine = create_engine(config.DB_URL, echo=True)
session = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))
Base = declarative_base()
Base.query = session.query_property() # для того что бы можно было обращатся к моделям напрямую
