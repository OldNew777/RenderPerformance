import logging
import os

log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'outputs', 'log.log')


def clear_log_file():
    with open(log_file, 'w') as f:
        pass


log_format = '%(asctime)-27s%(levelname)-10s%(message)s'
date_format = '[%Y-%m-%d %H:%M:%S]'
formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format)

logger = logging.getLogger(__file__)

file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
