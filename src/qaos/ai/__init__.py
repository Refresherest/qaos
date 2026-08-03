"""
QAOS AI Framework
"""

from .provider import AIProvider

from .registry import (
    register,
    get,
    all_providers,
)

from .engine import (
    AIEngine,
    engine,
)

from .providers import MockProvider

provider = MockProvider()
register(provider.name, provider)

__all__ = [
    "AIProvider",
    "AIEngine",
    "engine",
    "register",
    "get",
    "all_providers",
]