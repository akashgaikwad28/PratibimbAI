# backend\app\utils\logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pratibimbai.log")

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger  # prevent duplicate handlers

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # File (Standard handler to avoid WinError 32 on reload)
    file = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file)

    return logger
