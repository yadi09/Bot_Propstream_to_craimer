import logging

def setup_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # prevent duplicate logs

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"))

    logger.addHandler(console_handler)

    return logger
