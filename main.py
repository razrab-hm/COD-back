from fastapi import FastAPI
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
load_dotenv()
if __name__ == '__main__':
    print('hello')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    engine = create_engine(
        f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
    )
    print(engine)
