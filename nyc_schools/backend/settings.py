import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
FLASK_APP = os.getenv('FLASK_APP')
DEBUG = True
TESTING = True


TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_USER = os.getenv("TEST_DB_USER")
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
