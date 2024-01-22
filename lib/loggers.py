import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Log INFO and above to console

file_handler = logging.FileHandler('codx.log')
file_handler.setLevel(logging.DEBUG)  # Log DEBUG and above to file

logger = logging.getLogger(__name__)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.debug('This is a debug message')  # Only in file
logger.info('This is an info message')  # In both console and file