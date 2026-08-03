from qaos.scheduler.scheduler import scheduler
from qaos.scheduler.registry import get


class SchedulerManager:

    def add(self, name):
        job = get(name)

        if job is None:
            raise ValueError(
                f"Unknown job: {name}"
            )

        scheduler.schedule(job)

    def run(self):
        scheduler.run()


scheduler_manager = SchedulerManager()