"""
QAOS System Capability
"""


class SystemCapability:
    """
    Default capability.

    Executes planner Tasks, legacy Actions,
    and future executable objects.
    """

    name = "system"

    # ----------------------------------

    def execute(self, item):

        executable = item.action

        #
        # Determine display text
        #

        if hasattr(executable, "description"):

            text = executable.description

        elif hasattr(executable, "name"):

            text = executable.name

        else:

            text = str(executable)

        print(
            f"[System] Executing '{text}'"
        )

        #
        # Update execution state
        #

        if hasattr(executable, "start"):

            executable.start()

            print(f"[RUNNING] {text}")

        #
        # Actual execution hook
        #
        # (LLM/tool/plugin execution will live here later.)
        #

        if hasattr(executable, "complete"):

            executable.complete()

            print(f"[DONE]    {text}")

        return executable

    # ----------------------------------

    def __repr__(self):

        return "<SystemCapability>"


system_capability = SystemCapability()