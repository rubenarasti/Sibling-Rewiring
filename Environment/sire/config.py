import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class Config:
    secret_key_env = os.getenv('SECRET_KEY')
    if not secret_key_env:
        raise ValueError("No SECRET_KEY set, create the file .env with a variable named SECRET_KEY")
    SECRET_KEY = secret_key_env.encode()
    DEBUG = False

    @staticmethod
    def get_db_config():
        if os.getenv('IS_DOCKER', 'false') == 'true':
            return {
                'host': os.getenv('DATABASE_HOST', 'db'),
                'user': os.getenv('DATABASE_USER', 'root'),
                'password': os.getenv('DATABASE_PASSWORD', 'root'),
                'database': os.getenv('DATABASE_NAME', 'sire')
            }
        else:
            DATABASE_URL = os.getenv('DATABASE_URL')
            if DATABASE_URL:
                url = urlparse(DATABASE_URL)
                return {
                    'host': url.hostname,
                    'user': url.username,
                    'password': url.password,
                    'database': url.path[1:],
                    'port': url.port if url.port else 3306
                }
            else:
                return {
                    'host': os.getenv('DATABASE_HOST', 'localhost'),
                    'user': os.getenv('DATABASE_USER', 'root'),
                    'password': os.getenv('DATABASE_PASSWORD', 'root'),
                    'database': os.getenv('DATABASE_NAME', 'sire')
                }
            
            