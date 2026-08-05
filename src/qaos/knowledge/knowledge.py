"""
QAOS Knowledge
"""


class Knowledge:

    def __init__(
        self,
        title,
        category,
        content,
        source=None,
        tags=None,
    ):

        self.title = title
        self.category = category
        self.content = content
        self.source = source
        self.tags = tags or []

    def add_tag(self, tag):

        if tag not in self.tags:
            self.tags.append(tag)

    def __repr__(self):

        return (
            f"<Knowledge {self.title}>"
        )