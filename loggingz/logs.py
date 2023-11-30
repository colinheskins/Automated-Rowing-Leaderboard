import logging
import os

def setup_logger(logger_name, log_level, log_file):
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Use absolute path for the log file
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_file)
    
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
