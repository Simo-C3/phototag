import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from time import sleep

from .models import *
import os

DATABASE = 'postgresql'
USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = os.environ.get('POSTGRES_DB')

print(HOST)

DATABASE_URL = "{}://{}:{}@{}/{}".format(DATABASE,
                                         USER, PASSWORD, HOST, DB_NAME)

ECHO_LOG = False

engine = sqlalchemy.create_engine(DATABASE_URL, echo=ECHO_LOG)

retry_interval = 2
# 試行回数
tries = 4
for i in range(0, tries):
    try:
        Base.metadata.create_all(bind=engine)
        break
    except sqlalchemy.exc.OperationalError as e:
        if i + 1 == tries:
            raise e
        sleep(retry_interval)
        continue

SessionClass = sessionmaker(engine)


def get_db() -> Session:
    db = SessionClass()
    try:
        yield db
    finally:
        db.close()
