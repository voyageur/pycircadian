import argparse
import logging
import re


def init_config():
    global main_config

    parser = argparse.ArgumentParser(description="Systemd suspend-on-idle daemon")

    parser.add_argument("-f", "--config", type=str, default="/etc/pycircadian.conf",
                        help="configuration file path (default: %(default)s)")
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="increase logging level (can be repeated for info/debug)")

    args = parser.parse_args()

    level = logging.WARNING
    if args.verbosity >= 2:
        level = logging.DEBUG
    elif args.verbosity >= 1:
        level = logging.INFO
    logging.basicConfig(format='%(asctime)s %(message)s', level=level)

    # TODO: actually load config file
    main_config = {
        "max_cpu_load": 5,
        "process_block": re.compile("^dd$|^rsync$|^cp$|^mv$|^emerge$|^rdiff-backup$")
    }

    return main_config
