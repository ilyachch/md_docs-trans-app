import sys

from loguru import logger

logger.remove()
logger.add(sys.stdout, format='[{time:HH:mm:ss}] <lvl>{message}</lvl>', level='INFO')
logger.opt(colors=True)
