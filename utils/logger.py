import logging
import sys


def setup_logger():
    logger = logging.getLogger("JobAggregator")
    logger.setLevel(logging.INFO)

    # Create logs directory if it doesn't exist
    import os
    if not os.path.exists('logs'): os.makedirs('logs')

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')

    # ADD encoding='utf-8' HERE
    file_handler = logging.FileHandler('logs/scraper.log', encoding='utf-8')
    file_handler.setFormatter(formatter)

    # ADD stream=sys.stdout to ensure it handles the terminal output correctly
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()