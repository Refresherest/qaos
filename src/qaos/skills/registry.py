"""
QAOS Skill Registry
"""

class SkillRegistry:
    """Registry state owned by one skill lifecycle."""

    def __init__(self):
        self._skills = {}

    def register(self, skill):
        self._skills[skill.name] = skill

    def unregister(self, name):
        self._skills.pop(name, None)

    def get(self, name):
        return self._skills.get(name)

    def all(self):
        return self._skills


skill_registry = SkillRegistry()


def register(skill):
    """
    Register a Skill instance.
    """
    skill_registry.register(skill)


def unregister(name):
    """
    Remove a Skill.
    """
    skill_registry.unregister(name)


def get(name):
    """
    Retrieve a Skill by name.
    """
    return skill_registry.get(name)


def all():
    """
    Return all registered skills.
    """
    return skill_registry.all()
