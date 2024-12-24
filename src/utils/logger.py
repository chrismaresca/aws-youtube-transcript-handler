# -------------------------------------------------------------------------------- #
# Logger
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

import logging
import sys
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------------------------------------- #
# Logger Configuration
# -------------------------------------------------------------------------------- #

# Create logger
service_name = os.getenv("SERVICE_NAME")
if service_name is None:
    raise ValueError("SERVICE_NAME is not set")

# Create logger
logger = logging.getLogger(service_name)

# Get from environment or default to INFO
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, log_level, logging.INFO))

# Create stdout handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logger.level)

# Create formatter with function name
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s')
stdout_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(stdout_handler)
