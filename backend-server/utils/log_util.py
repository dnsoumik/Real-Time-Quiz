
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

LOG_FILE_PATH = './log/run.log'

class StreamToLogger:
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level

    def write(self, message):
        if message.strip():
            self.logger.log(self.log_level, message.strip())

    def flush(self):
        pass

# Basic log handler setup with rotation
rotationHandler = TimedRotatingFileHandler(
    LOG_FILE_PATH, when="H", interval=1
)
logging.basicConfig(
    format='| %(asctime)s | %(levelname).1s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.DEBUG,
    handlers=[rotationHandler]
)

# Redirect stdout and stderr to logger
sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO)
sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)

logging.info('Logging started.')

Log = logging
