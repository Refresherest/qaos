class Agent:
    """
    Base class for every QAOS agent.
    """

    def __init__(self, name, title, description):
        self.name = name
        self.title = title
        self.description = description

    def run(self):
        print(f"Running agent: {self.title}")

    def info(self):
        print("=" * 50)
        print(self.title)
        print("=" * 50)
        print(f"Name        : {self.name}")
        print(f"Description : {self.description}")