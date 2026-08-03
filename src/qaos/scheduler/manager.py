"""
QAOS Scheduler Manager
"""

from qaos.scheduler.registry import (
    register,
    unregister,
    get,
    all_jobs,
)


class SchedulerManager:

    def register(self, job):
        register(job)

    def unregister(self, name):
        unregister(name)

    def get(self, name):
        return get(name)

    def jobs(self):
        return all_jobs()

    def run(self, name):
        job = get(name)

        if job:
            job.run()

    def run_all(self):
        for job in all_jobs().values():
            job.run()


scheduler_manager = SchedulerManager()