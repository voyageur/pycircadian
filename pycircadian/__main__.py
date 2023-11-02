from pycircadian import config
from pycircadian import cpu_load, idle_sessions, process_block


def get_all_idle():
    sessions = idle_sessions.get_sessions()
    min_idle_tty = idle_sessions.get_min_idle_tty_sessions(sessions)
    print("Min TTY idle: {0}".format(min_idle_tty))
    min_idle_x11 = idle_sessions.get_min_idle_x11_sessions(sessions)
    print("Min X11 idle: {0}".format(min_idle_x11))
    blocking_processes = process_block.check_blocking_processes()
    print("Blocking processes: {0}".format(blocking_processes))
    system_loaded = cpu_load.check_load_avg()
    print("System load below threshold: {0}".format(system_loaded))


def circadian_main():
    config.init_config()
    # TODO
    get_all_idle()


if __name__ == "__main__":
    circadian_main()
