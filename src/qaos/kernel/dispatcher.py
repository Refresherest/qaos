"""
QAOS Command Dispatcher
"""

from qaos.commands.registry import COMMANDS


class Dispatcher:
    """Routes commands to their registered handlers."""

    def dispatch(self, command: str, *args) -> bool:
        handler = COMMANDS.get(command)

        if handler is None:
            print(f"Unknown command: {command}")
            return False

        handler(*args)
        return True
