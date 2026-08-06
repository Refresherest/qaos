"""
QAOS Action Manager
"""

from .registry import (
    register,
    get,
    all,
)

from .executor import (
    action_executor,
)


class ActionManager:

    def register(self, action):

        register(action)

    # ----------------------------------

    def get(self, name):

        return get(name)

    # ----------------------------------

    def actions(self):

        return all()

    # ----------------------------------

    def execute(self, action):

        return action_executor.execute(
            action
        )


action_manager = ActionManager()