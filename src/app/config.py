import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get('SECRET')
EXPIRATION_TIME = int(os.environ.get('EXPIRATION_TIME'))  # type: ignore
KAFKA_HOST = os.environ.get('KAFKA_HOST')
KAFKA_PORT = os.environ.get('KAFKA_PORT')
PRODUCE_TOPIC = os.environ.get('TOPIC')
