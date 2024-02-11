import os

from loguru import logger

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

logger.level(LOG_LEVEL)
