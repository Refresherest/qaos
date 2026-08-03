JOBS = {}


def register(name, job):
    JOBS[name] = job


def get(name):
    return JOBS.get(name)


def all():
    return JOBS