import logging
from pycircadian import config
from pycircadian import cpu_load, idle_actions, idle_sessions, net_connections, \
    process_block, sound_block


def check_all_idle():
    sessions = idle_sessions.get_sessions()
    min_idle_tty = idle_sessions.get_min_idle_tty_sessions(sessions)
    if min_idle_tty >= config.main_config["idle_time"]:
        return False
    min_idle_x11 = idle_sessions.get_min_idle_x11_sessions(sessions)
    if min_idle_x11 >= config.main_config["idle_time"]:
        return False

    blocking_processes = process_block.check_blocking_processes()
    if blocking_processes:
        return False
    system_loaded = cpu_load.check_load_avg()
    if system_loaded:
        return False
    active_net_connections = net_connections.check_net_connections()
    if active_net_connections:
        return False
    active_sound = sound_block.check_sound()
    if active_sound:
        return False

    can_idle = idle_actions.can_run_action()
    if not can_idle:
        return False

    logging.warn("System identified as idle")
    logging.info("Min TTY idle: {0}".format(min_idle_tty))
    logging.info("Min X11 idle: {0}".format(min_idle_x11))
    logging.info("Blocking processes: {0}".format(blocking_processes))
    logging.info("System load above threshold: {0}".format(system_loaded))
    logging.info("Active network connections: {0}".format(active_net_connections))
    logging.info("Sound playing: {0}".format(active_sound))
    logging.info("Can execute idle action: {0}".format(can_idle))
    return True


def circadian_main():
    config.init_config()
    # TODO
    check_all_idle()
    # idle_actions.run_action()


if __name__ == "__main__":
    circadian_main()
