import logging
from psutil import process_iter
from pycircadian import config


def check_blocking_processes() -> bool:
    """ Return True if a process running matches the block regex filter """
    regex = config.main_config["process_block"]
    found_proc = False

    for proc in process_iter():
        if regex.match(proc.name()):
            found_proc = True
            logging.info("Found blocking process: {0}".format(proc))
            break

    return found_proc
