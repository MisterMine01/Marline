import logging
import time
import os


def file_handler(folder) -> logging.FileHandler:
    file = logging.getLogger("File")
    new_handler = logging.FileHandler(
        os.path.join(folder, time.strftime("%Y.%m.%d-%H.%M.%S.log",
                                           time.localtime())))
    new_handler.formatter = file.handlers[0].formatter
    return new_handler


def setup(folder) -> logging.Logger:
    console = logging.getLogger("Console")
    console.addHandler(file_handler(folder))
    return console
