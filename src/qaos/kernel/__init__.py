"""
QAOS Kernel Package

The Kernel is the central execution layer of QAOS.
It receives requests from the CLI and delegates them
to the Dispatcher for execution.
"""

from .kernel import Kernel

__all__ = ["Kernel"]