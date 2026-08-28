"""
QAOS Skill Resolver
"""

from .registry import skill_registry


class SkillResolver:
    """
    Resolves the most appropriate
    skill for an incoming QueueItem.

    This initial implementation simply
    returns the first registered skill.

    Later it will use:

        - objective classification
        - capabilities
        - routing rules
        - confidence scores
    """

    def __init__(self, registry=None):
        self._registry = skill_registry if registry is None else registry

    def resolve(self, item):

        skills = self._registry.all()

        if not skills:

            raise RuntimeError(
                "No skills registered."
            )

        return next(
            iter(skills.values())
        )


skill_resolver = SkillResolver()
