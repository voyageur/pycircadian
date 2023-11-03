from signal import signal, SIGUSR1
from threading import Event
from pycircadian import config
from pycircadian.all_checks import check_all_idle


def usr1_handler(signum, frame):
    check_all_idle(False)


def circadian_main():
    config.init_config()

    signal(SIGUSR1, usr1_handler)

    main_loop = Event()
    while True:
        check_all_idle()
        main_loop.wait(60)


if __name__ == "__main__":
    circadian_main()
