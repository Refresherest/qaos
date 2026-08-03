"""
QAOS Task Manager
"""

from qaos.tasks.registry import register, get, all_tasks


class TaskManager:

    def register(self, name, task):
        register(name, task)

    def execute(self, name):
        task = get(name)

        if task is None:
            raise ValueError(f"Task '{name}' not found.")

        return task.execute()

    def count(self):
        return len(all_tasks())