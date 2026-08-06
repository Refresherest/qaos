"""
QAOS Worker
"""

from datetime import datetime


class Worker:

    def __init__(
        self,
        name,
        description="",
    ):

        self.name = name
        self.description = description

        self.busy = False

    # ---------------------------------

    def execute(self, item):

        self.busy = True

        item.status = "running"

        item.started = datetime.now()

        print(
            f"[Worker:{self.name}] "
            f"Executing '{item.objective}'"
        )

        #
        # Execute the assigned task
        #

        task = item.action

        if task is not None:

            print(
                f"[RUNNING] {task.description}"
            )

            task.start()

            #
            # Future:
            # AI
            # Skills
            # Council
            # Plugins
            # Actions
            #

            task.complete()

            print(
                f"[DONE]    {task.description}"
            )

        #
        # Complete queue item
        #

        item.status = "completed"

        item.completed = datetime.now()

        item.result = (
            f"Completed: {item.objective}"
        )

        self.busy = False

        return item

    # ---------------------------------

    def available(self):

        return not self.busy

    # ---------------------------------

    def __repr__(self):

        return (
            f"<Worker "
            f"{self.name} "
            f"busy={self.busy}>"
        )