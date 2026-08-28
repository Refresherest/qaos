"""
QAOS AI Framework
"""

from .provider import AIProvider
from .generation import GenerationEvidence

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
    "GenerationEvidence",
    "AIEngine",
    "engine",
    "register",
    "get",
    "all_providers",
]
