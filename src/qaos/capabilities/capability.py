"""
QAOS Capability
"""


class Capability:
    """
    Base class for all QAOS capabilities.
    """

    def __init__(
        self,
        name,
        description="",
    ):

        self.name = name
        self.description = description

        self._operations = {}

    # ----------------------------------

    def register(
        self,
        name,
        function,
    ):
        """
        Register an operation.
        """

        self._operations[name] = function

    # ----------------------------------

    def operations(self):

        return dict(self._operations)

    # ----------------------------------

    def execute(
        self,
        operation,
        *args,
        **kwargs,
    ):

        function = self._operations.get(
            operation
        )

        if function is None:

            raise RuntimeError(
                f"Operation '{operation}' "
                f"not found in capability "
                f"'{self.name}'."
            )

        return function(
            *args,
            **kwargs,
        )

    # ----------------------------------

    def __repr__(self):

        return (
            f"<Capability "
            f"{self.name}>"
        )