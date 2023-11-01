import logging
from pycircadian import idle_sessions

def init_config():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def get_all_idle():
    sessions = idle_sessions.get_sessions()
    min_idle_tty = idle_sessions.get_min_idle_tty_sessions(sessions)
    print(min_idle_tty)

def circadian_main():
    init_config()
    #TODO
    get_all_idle()

if __name__ == "__main__":
    circadian_main()
