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

    def execute(self, name):

        action = get(name)

        if action is None:
            raise ValueError(
                f"Unknown action: {name}"
            )

        capability = capability_manager.get(
            action.capability
        )

        if capability is None:
            raise ValueError(
                f"Unknown capability: "
                f"{action.capability}"
            )

        return capability.execute(
            action.operation,
            *action.args,
            **action.kwargs,
        )


action_manager = ActionManager()