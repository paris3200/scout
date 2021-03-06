"""Configuration settings for scout."""
import os

from sqlalchemy.ext.declarative import declarative_base

# Sets the log file to the path provided or defaults to the tmp folder.
LOGFILE = os.environ.get("LOGFILE", "/tmp/scoutlog")


# Database configuration
DATABASE = os.environ.get("DATABASE", "sqlite:///scout.db")
Base = declarative_base()
