"""
QAOS Skill Registry
"""

SKILLS = {}


def register(skill):
    """
    Register a Skill instance.
    """
    SKILLS[skill.name] = skill


def unregister(name):
    """
    Remove a Skill.
    """
    SKILLS.pop(name, None)


def get(name):
    """
    Retrieve a Skill by name.
    """
    return SKILLS.get(name)


def all():
    """
    Return all registered skills.
    """
    return SKILLS