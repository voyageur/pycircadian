# pycircadian
### A systemd suspend-on-idle daemon

This lightweight daemon will trigger suspend/sleep/hibernate automatically when a computer is idle, based on a series of checks.
It is aimed for systems with python and systemd, with minimal additional dependencies.

Possible checks (any can be disabled/enabled) include:
* X11 activity (screensaver, mouse, …)
* TTY activity (SSH sessions, terminals, …)
* Open SSH connections
* Open Samba connections
* Open NFS connections
* Active audio playback
* CPU load
* Running process blocking shutdown (compilations, video players, long file copies, …)

### Alternatives
Systemd itself has an IdleAction parameter, but this only works if user sessions correctly report the idle status to the system
(mostly limiting support to mostly Gnome and KDE).

pycircadian is heavily inspired by [circadian](https://github.com/mrmekon/circadian), but focused on systemd and written in Python.
Circadian covers other init systems but depends on external binaries calls, many external Rust packages (inherent to the language),
while pycircadian levels systemd DBUS interface and python system API to query the system,
providing a lightweight alternative with mostly built-in checks.

Note that as pycircadian requires systemd, it does not provide an automatic wakeup like circadian, as systemd itself provides this feature.

## Dependencies and installation
If you use Gentoo Linux, an ebuild is available in my [overlay](https://cafarelli.fr/cgi-bin/cgit.cgi/voyageur-overlay/tree/sys-power/pycircadian)

These are the dependencies to run pycircadian (basically most modern Linux systems):
* systemd (used for sessions tracking, suspend actions, ...)
* python>=3.11 with 2 non-core modules: dbus-python, psutil
* ALSA for sound detection
* (optional, for X11 idle detection) xprintidle, xssstate

You can install pycircadian and its python dependencies with usual command:
```
$ pip install .
```

Then install the configuration file and systemd service file (as root):
```
# cp resources/pycircadian.conf.in /etc/pycircadian.conf
# cp resources/pycircadian.service /lib/systemd/system/pycircadian.service
```

Edit the configuration file to match your preferences (idle time, idle action, heuristics to use, …)
Then enable the daemon (still as root):
```
# systemctl daemon-reload
# systemctl enable pycircadian.service
# systemctl start pycircadian.service
```
