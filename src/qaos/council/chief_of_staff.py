"""
AI Chief of Staff
"""

from .member import CouncilMember


class ChiefOfStaff(CouncilMember):

    def __init__(self, registry=None):
        super().__init__(
            name="chief_of_staff",
            title="AI Chief of Staff",
            description="Executive coordination and strategic oversight.",
            registry=registry,
        )

    def run(self):
        print("=" * 50)
        print("QAOS Executive Council")
        print("=" * 50)
        print()
        print(f"Agent : {self.title}")
        print("Status: Running")
        print()
        print("Executive Council successfully initialized.")
