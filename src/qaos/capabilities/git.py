"""
QAOS Git Capability
"""

import subprocess

from qaos.capabilities.base import Capability


class GitCapability(Capability):

    def __init__(self):
        super().__init__(
            name="git",
            description="Git source control capability.",
        )

    def execute(self, action, *args):

        if action == "status":
            command = ["git", "status"]

        elif action == "add":
            command = ["git", "add", "."]

        elif action == "commit":
            if len(args) < 1:
                raise ValueError(
                    "Commit message required."
                )

            command = [
                "git",
                "commit",
                "-m",
                args[0],
            ]

        elif action == "push":
            command = ["git", "push"]

        elif action == "pull":
            command = ["git", "pull"]

        elif action == "branch":
            command = ["git", "branch"]

        elif action == "checkout":
            if len(args) < 1:
                raise ValueError(
                    "Branch name required."
                )

            command = [
                "git",
                "checkout",
                args[0],
            ]

        elif action == "log":
            command = [
                "git",
                "log",
                "--oneline",
            ]

        else:
            raise ValueError(
                f"Unknown git action: {action}"
            )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return result.stdout or result.stderr