"""
QAOS Kernel
"""

from qaos.runtime import Runtime


class Kernel:
    """
    The Kernel is the entry point into the QAOS runtime.
    It delegates execution to the Runtime.
    """

    def __init__(self):
        self.runtime = Runtime()

    def execute(self, command: str) -> bool:
        return self.runtime.execute(command)