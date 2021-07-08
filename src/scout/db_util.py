"""Database Utilities."""
from sqlalchemy import create_engine

from . import config

ENGINE = create_engine(config.DATABASE)
