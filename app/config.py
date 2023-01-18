import os

from pydantic import BaseSettings, Field
from dotenv import load_dotenv
load_dotenv()


class Settings(BaseSettings):
    db_url: str = Field(os.getenv('DATABASE_URL'))


settings = Settings()
