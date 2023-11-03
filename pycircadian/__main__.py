import logging
from pycircadian import config
from pycircadian import cpu_load, idle_actions, idle_sessions, net_connections, \
    process_block, sound_block


def check_all_idle(print_status: bool = False):
    # With print_status, run all checks and do not trigger action
    log = getattr(logging, "warning")
    if not print_status:
        log = getattr(logging, "info")

    sessions = idle_sessions.get_sessions()
    min_idle_tty = idle_sessions.get_min_idle_tty_sessions(sessions)
    log("Min TTY idle: {0}".format(min_idle_tty))
    if min_idle_tty < config.main_config["idle_time"] and not print_status:
        return False
    min_idle_x11 = idle_sessions.get_min_idle_x11_sessions(sessions)
    log("Min X11 idle: {0}".format(min_idle_x11))
    if min_idle_x11 < config.main_config["idle_time"] and not print_status:
        return False

    blocking_processes = process_block.check_blocking_processes()
    log("Blocking processes: {0}".format(blocking_processes))
    if blocking_processes and not print_status:
        return False
    system_loaded = cpu_load.check_load_avg()
    log("System load above threshold: {0}".format(system_loaded))
    if system_loaded and not print_status:
        return False
    active_net_connections = net_connections.check_net_connections()
    log("Active network connections: {0}".format(active_net_connections))
    if active_net_connections and not print_status:
        return False
    active_sound = sound_block.check_sound()
    log("Sound playing: {0}".format(active_sound))
    if active_sound and not print_status:
        return False

    can_idle = idle_actions.can_run_action()
    log("Can execute idle action: {0}".format(can_idle))
    if not can_idle and not print_status:
        return False

    if not print_status:
        logging.warning("System identified as idle")
    return not print_status


def circadian_main():
    config.init_config()
    # TODO
    check_all_idle()
    check_all_idle(True)
    # idle_actions.run_action()


if __name__ == "__main__":
    circadian_main()
