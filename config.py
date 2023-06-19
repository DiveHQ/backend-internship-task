import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_FILE = os.path.join(PROJECT_DIR, 'api', 'database.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_FILE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_secret_key'
