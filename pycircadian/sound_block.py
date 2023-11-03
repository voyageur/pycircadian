import logging
import re
from pathlib import Path
from pycircadian import config

running_regex = re.compile("RUNNING")


def check_sound() -> bool:
    """ Return True if an ALSA device reports a running state """

    # Nothing to check
    if not config.main_config["audio_block"]:
        return False

    alsa = Path("/proc/asound")
    for a_card in alsa.glob("card*/pcm*/sub*"):
        a_state = (a_card / "status").read_text()

        if running_regex.search(a_state):
            logging.info("Active ALSA device: {0}".format(a_card))
            return True

    return False
