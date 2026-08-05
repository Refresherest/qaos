"""
QAOS Skill
"""

from qaos.actions import Action


class Skill:

    def __init__(
        self,
        name,
        description,
        handler=None,
        category="general",
        version="1.0",
    ):

        self.name = name
        self.description = description
        self.handler = handler
        self.category = category
        self.version = version

    def execute(self, *args, **kwargs):

        if self.handler is None:

            return None

        print(
            f"[Skill] Executing '{self.name}'"
        )

        return self.handler(
            *args,
            **kwargs,
        )

    def actions(self, objective):

        return []

    def info(self):

        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
        }

    def __repr__(self):

        return (
            f"<Skill "
            f"{self.name}"
            f" ({self.category})>"
        )