"""
QAOS Scheduler
"""


class Scheduler:

    def __init__(self):
        self.jobs = []

    def schedule(self, job):
        self.jobs.append(job)

    def run(self):
        for job in self.jobs:
            job.run()


scheduler = Scheduler()