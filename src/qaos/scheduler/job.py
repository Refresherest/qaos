class Job:
    """
    Base scheduled job.
    """

    name = "job"

    def run(self):
        raise NotImplementedError