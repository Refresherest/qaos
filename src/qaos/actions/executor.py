"""
QAOS Action Executor
"""

from qaos.logging import logger


class ActionExecutor:
    """
    Executes QAOS Actions.
    """

    def execute(self, action):

        logger.info(
            f"Executing action '{action.name}'"
        )

        try:

            result = action.execute()

            logger.info(
                f"Completed action '{action.name}'"
            )

            return result

        except Exception as error:

            logger.exception(
                f"Action '{action.name}' failed"
            )

            raise error


action_executor = ActionExecutor()