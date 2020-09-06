import os
import signal
import threading
from typing import Callable

# stolen from https://stackoverflow.com/questions/29604205/make-python-script-exit-after-x-seconds-of-inactivity

def kill():
    """
    kills the process
    """
    os.kill(os.getpid(), signal.SIGTERM)

class Watchdog():
        
    def __init__(self, timeout: float, on_alarm: Callable = kill, *args, **kwargs):
        """class that automatically runs function on_alarm(*args, **kwargs) after timeout seconds

        requires calling start() to start the watchdog

        Args:
            timeout (int): seconds to exit. Defaults to 10.
            on_alarm ([type], optional): function to call on exit. Defaults to killing the process.
        """
        self.timeout = timeout
        self.timer = None
        self.on_alarm = lambda: on_alarm(*args, **kwargs)

    def start(self):
        """
        start the watchdog.z
        starting the watchdog several times does not reset the timer.
        call refresh() to reset the timer.
        
        """
        if self.timer is None:
            self.timer = threading.Timer(self.timeout, self.on_alarm)
            self.timer.start()

    def stop(self):
        """
        stop the watchdog.
        """
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def refresh(self):
        """
        reset watchdog timer
        """
        if self.timer is not None:
             self.stop()
             self.start()
