"""
QAOS Executor Resolver
"""


class ExecutorResolver:

    def resolve(self, task_name):

        name = task_name.lower()

        if "memory" in name:
            return "Memory Manager"

        if "runtime" in name:
            return "AI Chief Technology Officer"

        if "ai" in name:
            return "AI Engine"

        if "plugin" in name:
            return "Plugin Manager"

        if "workflow" in name:
            return "Workflow Manager"

        return "Unknown"


resolver = ExecutorResolver()