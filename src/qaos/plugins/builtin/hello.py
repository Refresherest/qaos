"""
QAOS Built-in Hello Plugin
"""


class HelloPlugin:

    name = "hello"

    version = "1.0.0"

    description = "Example QAOS built-in plugin"

    def start(self):
        print("Hello Plugin started.")