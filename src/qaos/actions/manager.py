"""
QAOS Action Manager
"""

from .registry import (
    register,
    get,
    all,
)


class ActionManager:

    def register(self, action):

        register(action)

    def get(self, name):

        return get(name)

    def actions(self):

        return all()

    def execute(self, action):
        """
        Executes a QAOS Action.
        """

        return action.execute()


action_manager = ActionManager()