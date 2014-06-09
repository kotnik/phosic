import random
import string
import os
import sys
import logging
import logging.handlers
import subprocess
from subprocess import CalledProcessError

from colorama import Fore, Style
import setproctitle

log = logging.getLogger(__name__)

def generate_uniqid(length):
    return ''.join(
        random.choice(string.lowercase+string.digits) for i in range(length)
    )

def check_call(*args, **kwargs):
    """ Mimics behaviour of subprocess.check_call.

    Difference from check_call:
    * Logs the command
    * Logs command output
    * In case of errors logs command error
    * Returns normal output
    """
    log.debug("Executing command: %s" % subprocess.list2cmdline(args[0]))

    # Extract command stdin input from kwargs, if any.
    data = None
    if "data" in kwargs:
        data = kwargs["data"]
        del(kwargs["data"])

    kwargs.setdefault("close_fds", True)

    proc = subprocess.Popen(
        *args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.PIPE, **kwargs
    )
    (stdout_data, stderr_data) = proc.communicate(input=data)

    if stdout_data.strip():
        log.debug("OUT: %s" % stdout_data.strip().replace('\n', ' -- '))
    if stderr_data.strip():
        log.debug("ERR: %s" % stderr_data.strip().replace('\n', ' -- '))

    if proc.returncode != 0:
        log.debug("ERR CODE: %s" % proc.returncode)
        if stdout_data.strip():
            log.debug("OUT: %s" % stdout_data.strip().replace('\n', ' -- '))
        if stderr_data.strip():
            log.debug("ERR: %s" % stderr_data.strip().replace('\n', ' -- '))
        exc = CalledProcessError(returncode=proc.returncode, cmd=args)
        raise exc

    return stdout_data.strip()

def setup_logging(verbose=True, stderr=True, color=True, syslog=True, appname=None):
    """ Sets logging format. """

    setproctitle.setproctitle("phosic")

    logging.getLogger().setLevel(logging.DEBUG)

    if stderr:
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG if verbose else logging.INFO)
        if color:
            stream_format = ColoredFormatter(
                "%(asctime)s %(name)s %(levelname)s %(message)s"
            )
        else:
            stream_format = logging.Formatter(
                "%(asctime)s %(name)s %(levelname)s %(message)s"
            )
        stream.setFormatter(stream_format)
        logging.getLogger().addHandler(stream)

    if syslog:
        # Configure syslog.
        syslog = logging.handlers.SysLogHandler(
            address='/dev/log',
            facility=logging.handlers.SysLogHandler.LOG_DAEMON
        )
        syslog.setLevel(logging.DEBUG)
        syslog_format = SyslogFormatter(appname)
        syslog.setFormatter(syslog_format)
        logging.getLogger().addHandler(syslog)

    # Disable various verbose logging.
    logging.getLogger('ZooKeeper').setLevel(logging.ERROR)
    logging.getLogger('boto').setLevel(logging.CRITICAL)
    logging.getLogger('kazoo.protocol.connection').setLevel(logging.WARNING)
    logging.getLogger('kazoo.client').setLevel(logging.WARNING)
    logging.getLogger('protean').setLevel(logging.INFO)
    logging.getLogger('protean.storage').setLevel(logging.WARNING)


COLORS = {
    'DEBUG': Style.DIM,
    'INFO': Style.NORMAL,
    'WARNING': Style.BRIGHT,
    'ERROR': Fore.RED,
    'CRITICAL': Style.BRIGHT + Fore.RED,
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        return COLORS[record.levelname] + logging.Formatter.format(self, record) + Style.RESET_ALL


class SyslogFormatter(logging.Formatter):
    def __init__(self, appname=None):
        if appname is None:
            appname = os.path.basename(sys.argv[0])

        appname = "%s[%d]" % (
            appname,
            os.getpid()
            )

        logging.Formatter.__init__(
            self,
            "%(asctime)s " + appname + ": %(name)s: %(levelname)s %(message)s",
            "%b %d %H:%M:%S",
            )

    def format(self, record):
        return logging.Formatter.format(self, record).encode('utf-8').replace("\n", " | ")
