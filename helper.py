import logging
from logging.handlers import TimedRotatingFileHandler
import os
from pathlib import Path


logger = logging.getLogger('ABDI')
__log_init = False


def ensure_directory(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        logger.info(f"Directory '{dir_path}' created successfully.")


def get_logger():
    global __log_init
    global logger
    if not __log_init:
        import guide_config
        logger = init_logging(log_dir=guide_config.log_dir, log_level=guide_config.log_level)
        __log_init = True
        
    return logger


def init_logging(log_dir, log_level=logging.DEBUG):
    formatter = logging.Formatter(
        '%(levelname)1.1s %(asctime)s %(module)15s:%(lineno)03d %(funcName)15s) %(message)s',
        datefmt='%H:%M:%S')
    
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = os.path.join(log_dir, "abdi.log")
    file_handler = TimedRotatingFileHandler(log_path, when="d")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    global logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)    
    logger.setLevel(log_level)

    return logger
