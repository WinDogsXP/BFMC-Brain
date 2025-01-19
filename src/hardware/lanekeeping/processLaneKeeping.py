if __name__ == "__main__":
    import sys
    sys.path.insert(0, "../../..")

from src.templates.workerprocess import WorkerProcess
from src.lanekeeping.threads.threadLaneKeeping import threadLaneKeeping

class processLaneKeeping(WorkerProcess):
    """
    This new process subscribes to camera frames and sends commands to steer/speed the car.
    """

    def __init__(self, queueList, logging, debugging=False):
        self.queuesList = queueList
        self.logger = logging
        self.debugging = debugging
        # Call the parent constructor:
        super(processLaneKeeping, self).__init__(self.queuesList)

    def run(self):
        """
        We let the WorkerProcess handle thread initialization, then run.
        """
        super(processLaneKeeping, self).run()

    def _init_threads(self):
        """
        Initialize our lane‐keeping thread.
        """
        laneThread = threadLaneKeeping(self.queuesList, self.logger, self.debugging)
        self.threads.append(laneThread)


# ======================= EXAMPLE USAGE ===========================
if __name__ == "__main__":
    from multiprocessing import Queue
    import logging
    import time

    queueList = {
        "Critical": Queue(),
        "Warning":  Queue(),
        "General":  Queue(),
        "Config":   Queue(),
    }
    logger = logging.getLogger()
    process = processLaneKeeping(queueList, logger, debugging=True)
    process.daemon = True
    process.start()


    time.sleep(20)
    process.stop()
