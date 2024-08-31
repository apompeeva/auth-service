import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get('JWT_SECRET_POMPEEVA')
EXPIRATION_TIME = int(os.environ.get('JWT_EXPIRATION_TIME_POMPEEVA'))  # type: ignore

KAFKA_HOST = os.environ.get('KAFKA_HOST_POMPEEVA')
KAFKA_PORT = os.environ.get('KAFKA_PORT_POMPEEVA')
PRODUCE_TOPIC = os.environ.get('TOPIC_POMPEEVA')

DB_HOST = os.environ.get('DB_HOST_POMPEEVA')
DB_PORT = os.environ.get('DB_PORT_POMPEEVA')
DB_NAME = os.environ.get('DB_NAME_POMPEEVA')
DB_USER = os.environ.get('DB_USER_POMPEEVA')
DB_PASS = os.environ.get('DB_PASS_POMPEEVA')
