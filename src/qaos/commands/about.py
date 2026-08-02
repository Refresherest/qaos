"""
QAOS About Command
"""

from qaos.logging import get_logger
from qaos.version import VERSION


def execute():
    logger = get_logger()
    logger.info("Executing about command")

    print("=" * 50)
    print("QAOS")
    print("Qaasim April AI Operating System")
    print("=" * 50)
    print()
    print("Mission:")
    print("Build an extensible AI operating system")
    print("for intelligent assistants, automation,")
    print("knowledge management and applications.")
    print()
    print("Status : Active Development")
    print(f"Version: {VERSION}")