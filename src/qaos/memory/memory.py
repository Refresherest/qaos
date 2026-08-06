"""
QAOS Memory
"""


class Memory:

    def __init__(
        self,
        title,
        content,
        category="general",
    ):

        self.title = title
        self.content = content
        self.category = category

    def __repr__(self):

        return f"<Memory {self.title}>"