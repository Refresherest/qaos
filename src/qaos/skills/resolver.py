"""
QAOS Skill Resolver
"""

from .registry import all


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

    def resolve(self, item):

        skills = all()

        if not skills:

            raise RuntimeError(
                "No skills registered."
            )

        return next(
            iter(skills.values())
        )


skill_resolver = SkillResolver()