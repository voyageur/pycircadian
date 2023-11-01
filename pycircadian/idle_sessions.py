import dbus
import logging
import time

system_bus = dbus.SystemBus()
login1 = system_bus.get_object("org.freedesktop.login1","/org/freedesktop/login1")
login_manager = dbus.Interface(login1,"org.freedesktop.login1.Manager")

def unwrap_dbus(val):
    if isinstance(val, dbus.ByteArray):
        return "".join([str(x) for x in val])
    if isinstance(val, (dbus.Array, list, tuple)):
        return [unwrap_dbus(x) for x in val]
    if isinstance(val, (dbus.Dictionary, dict)):
        return dict([(unwrap_dbus(x), unwrap_dbus(y)) for x, y in val.items()])
    if isinstance(val, (dbus.ObjectPath, dbus.Signature, dbus.String)):
        return str(val)
    if isinstance(val, dbus.Boolean):
        return bool(val)
    if isinstance(val, (dbus.Int16, dbus.UInt16, dbus.Int32, dbus.UInt32, dbus.Int64, dbus.UInt64)):
        return int(val)
    if isinstance(val, dbus.Byte):
        return bytes([int(val)])
    return val 

def get_sessions():
    systemd_sessions = login_manager.ListSessions()
    sessions = []
    for session in systemd_sessions:
        dbus_session = system_bus.get_object("org.freedesktop.login1",session[-1])
        dbus_properties = dbus.Interface(dbus_session, 'org.freedesktop.DBus.Properties')
        # dbus_properties.Get("org.freedesktop.login1.Session", "IdleSinceHint")
        
        session_infos = unwrap_dbus(dbus_properties.GetAll("org.freedesktop.login1.Session"))
        logging.debug("Found session: {0}".format(session_infos))
        sessions.append(session_infos)
    return sessions

def get_min_idle_tty_sessions(sessions: list):
    min_idle_tty = 2678400;
    for session in sessions:
        if session["Type"] == "tty" and session["IdleHint"]:
            session_idle = int(time.clock_gettime(time.CLOCK_MONOTONIC) - session["IdleSinceHintMonotonic"] / 1e6)
            logging.debug("TTY session {0} idle for {1} seconds".format(session["Id"], session_idle))
            min_idle_tty = min(min_idle_tty, session_idle)
    return min_idle_tty;