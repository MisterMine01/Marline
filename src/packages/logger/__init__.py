import logging
import logging.config
from .setup import setup
from .hook import exception_hook
import os
import sys


def setup_log(log_folder: str) -> None:
    if not os.path.exists("logging.conf"):
        raise FileNotFoundError("logging.conf not found")
    if not os.path.isdir(log_folder):
        os.makedirs(log_folder, exist_ok=True)
    logging.config.fileConfig("logging.conf")
    logging.root = setup(log_folder)
    logging.info("Logger has been set up")
    sys.excepthook = exception_hook
