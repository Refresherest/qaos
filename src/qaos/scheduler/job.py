"""
QAOS Scheduled Job
"""


class Job:

    def __init__(
        self,
        name,
        callback,
        interval=0,
    ):
        self.name = name
        self.callback = callback
        self.interval = interval

    def run(self):
        self.callback()