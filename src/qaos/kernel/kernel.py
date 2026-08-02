"""
QAOS Kernel
"""

from qaos.kernel.dispatcher import Dispatcher


class Kernel:
    """
    Central execution engine for QAOS.
    """

    def __init__(self):
        self.dispatcher = Dispatcher()

    def execute(self, command: str) -> bool:
        return self.dispatcher.dispatch(command)