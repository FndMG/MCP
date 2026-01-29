from dotenv import load_dotenv
from os import getenv
import logging
import os
from logging.handlers import RotatingFileHandler

load_dotenv()

class Config:
    LOG_FILE_PATH = getenv("LOG_FILE_PATH", "logs/mcp-api-wrapper.log")
    LOG_MAX_BYTES = int(getenv("LOG_MAX_BYTES", "10485760"))
    LOG_BACKUP_COUNT = int(getenv("LOG_BACKUP_COUNT", "5"))
    TIME_OUT_SECONDS = int(getenv("TIME_OUT_SECONDS", "600"))
    API_ACCESS_TOKEN = getenv("API_ACCESS_TOKEN")
    API_SECRET_KEY = getenv("API_SECRET_KEY")

    _initialized = False

    @classmethod
    def init(cls):
        if cls._initialized:
            return
        cls._initialized = True

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        os.makedirs(os.path.dirname(cls.LOG_FILE_PATH), exist_ok=True)
        file_handler = RotatingFileHandler(
            cls.LOG_FILE_PATH,
            maxBytes=cls.LOG_MAX_BYTES,
            backupCount=cls.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
