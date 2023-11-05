from signal import signal, SIGUSR1
from sys import exit as sysexit
from threading import Event
from pycircadian import config
from pycircadian.all_checks import check_all_idle


def usr1_handler(signum, frame):
    check_all_idle(False)


def circadian_main():
    config.init_config()

    signal(SIGUSR1, usr1_handler)

    try:
        main_loop = Event()
        main_loop.wait(config.main_config["start_delay"])
        while True:
            check_all_idle()
            main_loop.wait(60)
    except KeyboardInterrupt:
        sysexit(0)


if __name__ == "__main__":
    circadian_main()
