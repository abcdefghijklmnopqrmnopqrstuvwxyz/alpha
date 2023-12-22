import multiprocessing
import os
import signal
import time


class Watchdog(multiprocessing.Process):
    """
    Watchdog Process

    Monitors the execution time of a list of processes and terminates them if the specified timeout is exceeded.
    """

    def __init__(self, timeout: int, processes: list):
        """
        Watchdog constructor.

        Args:
            timeout (int): The maximum allowed execution time for the monitored processes in seconds.
            processes (list): A list of multiprocessing.Process pids to monitor and terminate.

        Raises:
            TypeError: If the provided timeout is not an integer or processes is not a list.
        """
        if not isinstance(timeout, int) or not isinstance(processes, list):
            raise TypeError
        super().__init__()
        self.timeout = timeout
        self.processes = processes

    def run(self):
        """
        Overrides the run method of multiprocessing.Process.

        Monitors the processes and terminates them if the specified timeout is exceeded.
        """

        start_time = time.time() + self.timeout

        while time.time() < start_time:
            pass

        for process in self.processes:
            os.kill(process, signal.SIGTERM)
