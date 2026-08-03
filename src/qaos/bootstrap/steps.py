"""
QAOS Bootstrap Steps
"""

from qaos.logging import logger
from qaos.plugins import plugin_manager


def initialize_logger():
    logger.info("Logger initialized")


def initialize_plugins():
    plugin_manager.initialize()