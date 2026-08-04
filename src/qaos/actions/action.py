class Action:
    """
    Represents one executable action.
    """

    def __init__(
        self,
        name,
        capability,
        operation,
        *args,
        **kwargs,
    ):
        self.name = name
        self.capability = capability
        self.operation = operation
        self.args = args
        self.kwargs = kwargs