import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get('SECRET')
EXPIRATION_TIME = int(os.environ.get('EXPIRATION_TIME'))  # type: ignore

KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')
PRODUCE_TOPIC = os.environ.get('TOPIC')

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
