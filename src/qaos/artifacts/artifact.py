"""
QAOS Artifact
"""


class Artifact:

    def __init__(
        self,
        title,
        artifact_type,
        creator,
        objective,
        content,
    ):

        self.title = title
        self.artifact_type = artifact_type
        self.creator = creator
        self.objective = objective
        self.content = content

    def __repr__(self):

        return f"<Artifact {self.title}>"