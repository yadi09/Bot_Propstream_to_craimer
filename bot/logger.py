import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(name="bot"):
    os.makedirs("logs", exist_ok=True)
    log_file = f"logs/{name}_{datetime.now().strftime('%Y-%m-%d')}.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # prevent duplicate logs

    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
