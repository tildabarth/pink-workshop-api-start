import datetime as dt
import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings


# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    host: str = os.getenv('HOST', '0.0.0.0')
    port: int = os.getenv('PORT', 8000)
    datetime_format: str = os.getenv('DATETIME_FORMAT', '%Y-%m-%dT%H:%M:%SZ')
    api_prefix: str = os.getenv('API_PREFIX', '/api/v1')


@lru_cache
def get_settings():
    """Get core settings."""
    return Settings()


def get_strftime(date_obj: dt.datetime) -> str:
    """Get datetime as string using custom format from settings."""
    return date_obj.strftime(get_settings().datetime_format)


def get_strptime(date_string: str) -> dt.datetime:
    """Get datetime from string using custom format from settings."""
    return dt.datetime.strptime(date_string, get_settings().datetime_format)
