"""
QAOS AI Provider Registry
"""

PROVIDERS = {}


def register(name: str, provider):
    """
    Register an AI provider.
    """
    PROVIDERS[name] = provider


def get(name: str):
    """
    Retrieve a registered AI provider.
    """
    return PROVIDERS.get(name)


def all_providers():

    return PROVIDERS
    
   