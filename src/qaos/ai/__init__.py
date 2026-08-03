print("1 - importing provider")
from .provider import AIProvider

print("2 - importing registry")
from .registry import register, get, all

print("3 - importing engine")
from .engine import AIEngine, engine

print("4 - importing providers")
from .providers import MockProvider

print("5 - creating provider")
provider = MockProvider()

print("6 - registering provider")
register("mock", provider)

print("7 - registration complete")

__all__ = [
    "AIProvider",
    "AIEngine",
    "engine",
    "register",
    "get",
    "all",
]