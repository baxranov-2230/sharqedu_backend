import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    DB_USER: str = os.getenv('DB_USER')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_PORT: str = os.getenv('DB_PORT')
    DB_NAME: str = os.getenv('DB_NAME')

    ACCESS_SECRET_KEY: str=os.getenv('ACCESS_SECRET_KEY')
    REFRESH_SECRET_KEY: str=os.getenv('REFRESH_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_DAYS: int=os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')
    ALGORITHM: str=os.getenv('ALGORITHM')


    @property
    def connection_string(self):
        values=self.model_dump()
        return (f'postgresql+asyncpg://'
                f'{values["DB_USER"]}:'
                f'{values["DB_PASSWORD"]}@'
                f'{values["DB_HOST"]}:{values["DB_PORT"]}/'
                f'{values["DB_NAME"]}')


settings=Settings()