"""Configuration settings for scout."""

import os

# Sets the log file to the path provided or defaults to the tmp folder.
LOGFILE = os.environ.get("LOGFILE", "/tmp/scoutlog")
