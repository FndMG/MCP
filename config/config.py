from dotenv import load_dotenv
from os import getenv
import logging
import os
from logging.handlers import RotatingFileHandler

class Config:
    LOG_FILE_PATH = getenv("LOG_FILE_PATH", "logs/mcp-api-wrapper.log")
    LOG_MAX_BYTES = int(getenv("LOG_MAX_BYTES", "10485760"))
    LOG_BACKUP_COUNT = int(getenv("LOG_BACKUP_COUNT", "5"))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    load_dotenv()

    TIME_OUT_SECONDS = int(getenv("TIME_OUT_SECONDS", "600"))

    API_ACCESS_TOKEN = getenv("API_ACCESS_TOKEN")
    API_SECRET_KEY = getenv("API_SECRET_KEY")
