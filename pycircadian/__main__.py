from pycircadian import config
from pycircadian import cpu_load, idle_actions, idle_sessions, net_connections, process_block


def get_all_idle():
    sessions = idle_sessions.get_sessions()
    min_idle_tty = idle_sessions.get_min_idle_tty_sessions(sessions)
    print("Min TTY idle: {0}".format(min_idle_tty))
    min_idle_x11 = idle_sessions.get_min_idle_x11_sessions(sessions)
    print("Min X11 idle: {0}".format(min_idle_x11))
    blocking_processes = process_block.check_blocking_processes()
    print("Blocking processes: {0}".format(blocking_processes))
    system_loaded = cpu_load.check_load_avg()
    print("System load above threshold: {0}".format(system_loaded))
    active_net_connections = net_connections.check_net_connections()
    print("Active network connections: {0}".format(active_net_connections))
    can_idle = idle_actions.can_run_action()
    print("Can execute idle action: {0}".format(can_idle))


def circadian_main():
    config.init_config()
    # TODO
    get_all_idle()
    # idle_actions.run_action()


if __name__ == "__main__":
    circadian_main()
