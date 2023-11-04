import dbus
import logging
from pycircadian import config

ORG = "org.freedesktop.login1"
PATH = "/org/freedesktop/login1"
MANAGER_IFACE = "org.freedesktop.login1.Manager"

# One month should be enough
LONG_IDLE = 2678400

system_bus = dbus.SystemBus()
login1 = system_bus.get_object(ORG, PATH)
login_manager = dbus.Interface(login1, MANAGER_IFACE)


def can_run_action():
    action_conf = config.main_config["action"]
    can_action = getattr(login_manager, "Can" + action_conf)
    answer = can_action()
    if (answer):
        logging.info("Can invoke idle action {0}".format(action_conf))
    else:
        logging.warn("Not allowed to call idle action {0}".format(action_conf))

    return answer


def run_action():
    action_conf = config.main_config["action"]
    action = getattr(login_manager, action_conf)
    logging.info("Invoking idle action {0}".format(action_conf))
    # Non-interactive
    action(False)
