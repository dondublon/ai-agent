from loguru import logger
from dotenv import load_dotenv
from sys import stderr
from os import getenv
load_dotenv()
logger.remove()
logger.add(stderr, level=getenv("LOG_LEVEL", "INFO"))
    