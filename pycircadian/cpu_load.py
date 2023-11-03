import logging
from os import getloadavg
from pycircadian import config


def check_load_avg() -> bool:
    """ Return True if 1-minute load average is above configured value """
    load_avg = getloadavg()
    logging.info("System load average: {0}".format(load_avg))
    return load_avg[0] > config.main_config["max_cpu_load"]
