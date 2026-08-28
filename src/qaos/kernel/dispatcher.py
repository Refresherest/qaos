"""
QAOS Command Dispatcher
"""

from qaos.commands.registry import COMMANDS


class Dispatcher:
    """Routes commands to their registered handlers."""

    def __init__(self, commands=None):
        self._commands = COMMANDS if commands is None else commands

    def dispatch(self, command: str, *args) -> bool:
        handler = self._commands.get(command)

        if handler is None:
            print(f"Unknown command: {command}")
            return False

        handler(*args)
        return True
