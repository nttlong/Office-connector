import logging
import logging.handlers
import os.path
import pathlib
import sys

current_dir= pathlib.Path(sys.executable).parent.__str__()
log_file_name = os.path.join(current_dir, "codx.log")  # Replace with your desired filename
max_bytes = 10 * 1024  # 10K bytes
backup_count = 5

# Create a formatter that includes timestamp and log level
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a rotating file handler with the specified settings
handler = logging.handlers.RotatingFileHandler(
    filename=log_file_name,
    maxBytes=max_bytes,
    backupCount=backup_count
)
handler.setFormatter(formatter)

# Add the handler to the root logger
logger = logging.getLogger()
logger.addHandler(handler)

# Set the logging level (e.g., INFO, DEBUG, WARNING)
logger.setLevel(logging.INFO)  # Adjust as needed