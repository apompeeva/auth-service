import os

from dotenv import load_dotenv

load_dotenv()

SECRET = os.environ.get('SECRET')
EXPIRATION_TIME = int(os.environ.get('EXPIRATION_TIME'))  # type: ignore
