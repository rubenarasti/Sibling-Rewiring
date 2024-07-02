import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    secret_key_env = os.getenv('SECRET_KEY')
    if not secret_key_env:
        raise ValueError("No SECRET_KEY set, create the file .env with a variable named SECRET_KEY")
    SECRET_KEY = secret_key_env.encode()
    DEBUG = True
    
