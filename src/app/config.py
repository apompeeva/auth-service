import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get('SECRET')
EXPIRATION_TIME = os.environ.get('EXPIRATION_TIME')
