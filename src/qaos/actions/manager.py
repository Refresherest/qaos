"""
QAOS Action Manager
"""

from .registry import (
    register,
    get,
    all,
)

from qaos.capabilities import capability_manager


class ActionManager:

    def register(self, action):

        register(action)

    def get(self, name):

        return get(name)

    def actions(self):

        return all()

    def execute(self, action):

        capability = capability_manager.get(
            action.capability
        )

        if capability is None:

            raise RuntimeError(
                f"Capability '{action.capability}' "
                f"not found."
            )

        print(
            f"[Action] {action.name}"
        )

        return capability.execute(
            action.operation,
            *action.args,
            **action.kwargs,
        )


action_manager = ActionManager()