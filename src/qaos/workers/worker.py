"""
QAOS Worker
"""

from qaos.actions import action_manager


class Worker:

    def __init__(self, name):
        self.name = name

    def execute(self, item):

        item.status = "running"

        if item.action:

            item.result = action_manager.execute(
                item.action
            )

        item.status = "completed"

        return item.result

    def __repr__(self):
        return f"<Worker {self.name}>"