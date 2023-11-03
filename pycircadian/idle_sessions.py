import dbus
import logging
import time
from os.path import expanduser
from subprocess import check_output, CalledProcessError
from pycircadian import config

ORG = "org.freedesktop.login1"
PATH = "/org/freedesktop/login1"
MANAGER_IFACE = "org.freedesktop.login1.Manager"
SESSION_IFACE = "org.freedesktop.login1.Session"
DBUS_PROP_IFACE = "org.freedesktop.DBus.Properties"

# One month should be enough
LONG_IDLE = 2678400

system_bus = dbus.SystemBus()
login1 = system_bus.get_object(ORG, PATH)
login_manager = dbus.Interface(login1, MANAGER_IFACE)


def _unwrap_dbus(val):
    if isinstance(val, dbus.ByteArray):
        return "".join([str(x) for x in val])
    if isinstance(val, (dbus.Array, list, tuple)):
        return [_unwrap_dbus(x) for x in val]
    if isinstance(val, (dbus.Dictionary, dict)):
        return dict([(_unwrap_dbus(x), _unwrap_dbus(y)) for x, y in val.items()])
    if isinstance(val, (dbus.ObjectPath, dbus.Signature, dbus.String)):
        return str(val)
    if isinstance(val, dbus.Boolean):
        return bool(val)
    if isinstance(val, (dbus.Int16, dbus.UInt16, dbus.Int32, dbus.UInt32, dbus.Int64, dbus.UInt64)):
        return int(val)
    if isinstance(val, dbus.Byte):
        return bytes([int(val)])
    return val


def get_sessions() -> list:
    systemd_sessions = login_manager.ListSessions()
    sessions = []
    for session in systemd_sessions:
        dbus_session = system_bus.get_object(ORG, session[-1])
        dbus_properties = dbus.Interface(dbus_session, DBUS_PROP_IFACE)
        # dbus_properties.Get(SESSION_IFACE, "IdleSinceHint")

        session_infos = _unwrap_dbus(dbus_properties.GetAll(SESSION_IFACE))
        logging.debug("Found session: {0}".format(session_infos))
        sessions.append(session_infos)
    return sessions


def get_min_idle_tty_sessions(sessions: list) -> int:
    min_idle_tty = LONG_IDLE

    # Nothing to check
    if not config.main_config["tty_input"]:
        return min_idle_tty

    for session in sessions:
        if session["Type"] == "tty" and session["IdleHint"]:
            session_idle = int(time.clock_gettime(time.CLOCK_MONOTONIC) - session["IdleSinceHintMonotonic"] / 1e6)
            logging.debug("TTY session {0} idle for {1} seconds".format(session["Id"], session_idle))
            min_idle_tty = min(min_idle_tty, session_idle)

    return min_idle_tty


def _run_x_command(command: list, env: dict) -> int:
    retval = LONG_IDLE
    try:
        output = check_output(command, env=env)
        retval = int(int(output) / 1e3) + 1
    except (CalledProcessError, FileNotFoundError) as error:
        logging.error("{0} run failed, error: {1}".format(command, error))
    return retval


def get_min_idle_x11_sessions(sessions: list) -> int:
    min_idle_x11 = LONG_IDLE

    # Nothing to check
    if not config.main_config["x11_input"]:
        return min_idle_x11

    for session in sessions:
        if session["Type"] == "x11":
            user_env = {"DISPLAY": session["Display"],
                        "XAUTHORITY": expanduser("~{0}/.Xauthority".format(session["Name"]))
                        }
            # TODO: conditional run
            xprintidle = _run_x_command(["xprintidle"], user_env)
            xssstate = _run_x_command(["xssstate", "-i"], user_env)
            logging.debug("Found X11 session {0}, idle time: xprintidle={1}, xsssate={2})"
                          .format(session["Id"], xprintidle, xssstate))
            min_idle_x11 = min(min_idle_x11, xprintidle, xssstate)

    return min_idle_x11
