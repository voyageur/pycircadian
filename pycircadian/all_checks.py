import logging
from pycircadian import config
from pycircadian import cpu_load, idle_actions, idle_sessions, net_connections, \
    process_block, sound_block


def check_all_idle(action: bool = True):
    # With action = False, run all checks and do not trigger action
    log = getattr(logging, "warning")
    if action:
        log = getattr(logging, "info")

    sessions = idle_sessions.get_sessions()
    min_idle_tty = idle_sessions.get_min_idle_tty_sessions(sessions)
    log("Min TTY idle: {0}".format(min_idle_tty))
    if min_idle_tty < config.main_config["idle_time"] and action:
        return False
    min_idle_x11 = idle_sessions.get_min_idle_x11_sessions(sessions)
    log("Min X11 idle: {0}".format(min_idle_x11))
    if min_idle_x11 < config.main_config["idle_time"] and action:
        return False

    blocking_processes = process_block.check_blocking_processes()
    log("Blocking processes: {0}".format(blocking_processes))
    if blocking_processes and action:
        return False
    system_loaded = cpu_load.check_load_avg()
    log("System load above threshold: {0}".format(system_loaded))
    if system_loaded and action:
        return False
    active_net_connections = net_connections.check_net_connections()
    log("Active network connections: {0}".format(active_net_connections))
    if active_net_connections and action:
        return False
    active_sound = sound_block.check_sound()
    log("Sound playing: {0}".format(active_sound))
    if active_sound and action:
        return False

    can_idle = idle_actions.can_run_action()
    log("Can execute idle action: {0}".format(can_idle))
    if not can_idle and action:
        return False

    if action:
        logging.warning("System identified as idle")
        idle_actions.run_action()
    return action
