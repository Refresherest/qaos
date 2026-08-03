from .registry import steps


class BootManager:

    def boot(self):
        for step in steps():
            step()


boot_manager = BootManager()