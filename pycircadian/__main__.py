from pycircadian import config
from pycircadian.all_checks import check_all_idle


def circadian_main():
    config.init_config()
    # TODO
    check_all_idle()
    check_all_idle(True)
    # idle_actions.run_action()


if __name__ == "__main__":
    circadian_main()
