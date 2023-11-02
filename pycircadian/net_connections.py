import logging
import psutil
from pycircadian import config


def check_net_connections() -> bool:
    """ Return True if system has active net connections"""
    nfs_block = config.main_config["nfs_block"]
    net_block_regex = config.main_config["net_block_regex"]

    # Skip process names if we do not check SSH/SMB
    if net_block_regex:
        proc_names = {}
        for p in psutil.process_iter(['pid', 'name']):
            proc_names[p.info['pid']] = p.info['name']

    for conn in psutil.net_connections(kind='inet'):
        if nfs_block and (conn.laddr.port == 2049 or
                          (conn.raddr and conn.raddr.port == 2049)):
            logging.info("Found NFS connection: {0}".format(conn))
            return True
        if net_block_regex and (conn.pid in proc_names and
                                net_block_regex.match(proc_names.get(conn.pid))):
            logging.info("Found SSH/SMB connection: {0}".format(conn))
            return True

    return False
