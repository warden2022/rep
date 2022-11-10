from pydantic import BaseSettings, SecretStr
import os

class Settings(BaseSettings):
    bot_token = os.getenv('tmTOKEN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()