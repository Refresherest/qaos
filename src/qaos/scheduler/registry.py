"""
QAOS Scheduler Registry
"""

JOBS = {}


def register(job):
    JOBS[job.name] = job


def unregister(name):
    JOBS.pop(name, None)


def get(name):
    return JOBS.get(name)


def all_jobs():
    return JOBS