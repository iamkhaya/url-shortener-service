"""
Utils for rest services
"""
import logging
import math
import os
import signal
import threading
import time

import six

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")


def remove_none_from_dict(d):
    """
    Recursively remove None values from dictionaries.
    Mostly for swagger response validation purposes, swagger doesn't really have support
    for "string or null" type stuff.
    """
    if isinstance(d, dict):
        return dict(
            (k, remove_none_from_dict(v))
            for k, v in six.iteritems(d)
            if v is not None and remove_none_from_dict(v) is not None
        )
    elif isinstance(d, list):
        return [remove_none_from_dict(i) for i in d]
    else:
        return d


class Notify(threading.Thread):
    """
    Notify implements a polling file tracker, due to issues with
    mounting docker volumes from the host into the running container
    which breaks inotify events from being fired inside the container.

    This breaks our development workflow, as nothing gets reloaded when
    it should. Sadly, using the `--reload` flag for gunicorn creates a
    reload spin cycle due to a potential bug in xhyve [1], which until
    it is resolved, means we can't use the built in reload functionality.

    [1]: https://github.com/mist64/xhyve/issues/131
    """

    def __init__(self, watch_base=".", file_mask=".py"):
        super(Notify, self).__init__()  # pylint: disable=super-with-arguments
        self.setDaemon(True)
        self.watch_base = watch_base
        self.file_mask = file_mask
        self.watchlist = {}
        self.first_run = True

    def run(self):
        while 1:
            if self.update_watchlist():
                self.reload_parent()
            time.sleep(1)

    def update_watchlist(self):
        """
        Walk the tree from the base directory, stat'ing the `self.file_mask`
        specified files, and if they've been modified, or created, flag that
        there has been modifications made in order to reload the parent.
        """
        modified = False
        for parent, _dir, files in os.walk(self.watch_base):
            for filename in files:
                if filename.endswith(self.file_mask):
                    filepath = os.path.join(parent, filename)
                    mtime = int(math.floor(os.stat(filepath).st_mtime))
                    if filepath not in self.watchlist or self.watchlist[filepath] != mtime:  # noqa
                        logging.info("[Modified] %s, %s", filepath, mtime)
                        modified = True
                    self.watchlist[filepath] = mtime
        if self.first_run:
            self.first_run = False
            return False
        return modified

    def reload_parent(self):
        """
        Send the SIGHUP signal to the parent PID (gunicorn master),
        which causes a reload of the workers.
        """
        logging.info("Sending SIHGUP to PPID<%s>", os.getppid())
        os.kill(os.getppid(), signal.SIGHUP)
