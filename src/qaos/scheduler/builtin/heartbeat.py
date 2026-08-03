from qaos.scheduler import Job
from qaos.logging import logger


class HeartbeatJob(Job):

    name = "heartbeat"

    def run(self):
        logger.info("Heartbeat job executed")