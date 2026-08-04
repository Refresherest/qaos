"""
QAOS Skill
"""


class Skill:

    def __init__(self, name, description, handler):

        self.name = name
        self.description = description
        self.handler = handler

    def execute(self, *args, **kwargs):

        return self.handler(*args, **kwargs)

    def __repr__(self):

        return f"<Skill {self.name}>"