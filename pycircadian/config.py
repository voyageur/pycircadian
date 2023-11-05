import argparse
import logging
import re
import sys
import tomllib


def _load_config_file(file_path: str) -> dict:
    toml_config = {}
    try:
        with open(file_path, "rb") as f:
            toml_config = tomllib.load(f)
    except FileNotFoundError:
        logging.critical("Configuration file \"{0}\" not found".format(file_path))
        sys.exit(1)
    except tomllib.TOMLDecodeError as toml_err:
        logging.critical("Configuration file \"{0}\" incorrect format:\n    {1}".format(file_path, toml_err))
        sys.exit(1)

    return toml_config


def init_config():
    global main_config

    parser = argparse.ArgumentParser(description="Systemd suspend-on-idle daemon")

    parser.add_argument("-f", "--config", type=str, default="/etc/pycircadian.conf",
                        help="configuration file path (default: %(default)s)")
    parser.add_argument("-v", "--verbosity", action="count",
                        help="increase logging level (can be repeated for info/debug)")

    args = parser.parse_args()

    file_conf = _load_config_file(args.config)

    if (args.verbosity):
        verbosity = args.verbosity
    elif (file_conf.get("settings").get("verbosity")):
        verbosity = file_conf.get("settings").get("verbosity")
    else:
        verbosity = 0

    level = logging.WARNING
    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity >= 1:
        level = logging.INFO
    logging.basicConfig(format='[%(levelname)s] %(message)s', level=level)

    # Default options
    main_config = {
        "tty_input": True,
        "x11_input": True,
        "net_block_regex": re.compile("(ssh)d?"),
        "nfs_block": False,
        "audio_block": True,
        "max_cpu_load": 1,
        "process_block": re.compile("^(cp|dd|mv|rsync)$"),
        "idle_time": 7200,
        "start_delay": 0,
        "action": "suspend"
    }

    for entry in ["tty_input", "x11_input", "nfs_block", "audio_block"]:
        value = file_conf.get("idle_checks").get(entry)
        if value is not None:
            main_config[entry] = value
    conf_max_cpu_load = file_conf.get("idle_checks").get("max_cpu_load")
    if conf_max_cpu_load:
        main_config["max_cpu_load"] = float(conf_max_cpu_load)
    conf_process_block = file_conf.get("idle_checks").get("process_block")
    if isinstance(conf_process_block, str):
        if conf_process_block != "":
            main_config["process_block"] = re.compile(conf_process_block)
        else:
            main_config["process_block"] = None

    # Regex for SSH/SMB
    ssh_block = "ssh"
    smb_block = None
    if file_conf.get("idle_checks").get("ssh_block") is not None:
        ssh_block = "ssh" if file_conf.get("idle_checks").get("ssh_block") else None
    if file_conf.get("idle_checks").get("smb_block") is not None:
        smb_block = "smb" if file_conf.get("idle_checks").get("smb_block") else None
    if (ssh_block or smb_block):
        main_config["net_block_regex"] = re.compile("({0})d?".format("|".join(filter(None, [ssh_block, smb_block]))))
    else:
        main_config["net_block_regex"] = None

    idle_time = file_conf.get("actions").get("idle_time")
    if idle_time:
        seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        main_config["idle_time"] = int(idle_time[:-1]) * seconds_per_unit[idle_time[-1]]
    start_delay = file_conf.get("actions").get("start_delay")
    if start_delay:
        seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        main_config["start_delay"] = int(start_delay[:-1]) * seconds_per_unit[start_delay[-1]]
    idle_action = file_conf.get("actions").get("on_idle")
    if idle_action:
        main_config["action"] = idle_action

    # TODO checks for xssstate etc

    if main_config["action"] not in ["Suspend", "Hibernate", "HybridSleep", "SuspendThenHibernate"]:
        logging.critical("Incorrect idle action {0} in configuration file".format(main_config["action"]))
        sys.exit(1)

    logging.info("Configuration loaded and valid")
    logging.debug("Loaded config: {0}".format(main_config))
    return main_config
