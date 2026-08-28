"""
QAOS Kernel
"""

from qaos.config import create_configuration
from qaos.core import create_runtime
from qaos.kernel.dispatcher import Dispatcher


class Kernel:
    """
    The Kernel is the entry point into the QAOS runtime.
    It delegates execution to the Runtime.
    """

    def __init__(
        self,
        configuration=None,
        *,
        logger=None,
        event_bus=None,
        executive=None,
        dispatcher=None,
    ):
        configuration = configuration or create_configuration()
        self.runtime = create_runtime(
            configuration,
            logger=logger,
            event_bus=event_bus,
            executive=executive,
        )
        self.dispatcher = Dispatcher() if dispatcher is None else dispatcher

    def execute(self, command: str, *args) -> bool:
        return self.dispatcher.dispatch(command, *args)
