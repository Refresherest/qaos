"""
QAOS Filesystem Capability
"""

from pathlib import Path

from qaos.capabilities import Capability


class FilesystemCapability(Capability):

    def __init__(self):
        super().__init__(
            name="filesystem",
            description="Filesystem operations",
        )

    def execute(
        self,
        action,
        *args,
    ):

        if action == "read":
            return self.read(args[0])

        if action == "write":
            return self.write(args[0], args[1])

        if action == "append":
            return self.append(args[0], args[1])

        if action == "exists":
            return self.exists(args[0])

        if action == "mkdir":
            return self.mkdir(args[0])

        if action == "delete":
            return self.delete(args[0])

        if action == "list":
            return self.list(args[0])

        raise ValueError(
            f"Unknown filesystem action: {action}"
        )

    def read(self, path):

        return Path(path).read_text(
            encoding="utf-8",
        )

    def write(
        self,
        path,
        text,
    ):

        Path(path).write_text(
            text,
            encoding="utf-8",
        )

    def append(
        self,
        path,
        text,
    ):

        with open(
            path,
            "a",
            encoding="utf-8",
        ) as file:

            file.write(text)

    def exists(self, path):

        return Path(path).exists()

    def mkdir(self, path):

        Path(path).mkdir(
            parents=True,
            exist_ok=True,
        )

    def delete(self, path):

        p = Path(path)

        if p.exists():

            p.unlink()

    def list(self, path="."):

        return [
            str(item)
            for item in Path(path).iterdir()
        ]