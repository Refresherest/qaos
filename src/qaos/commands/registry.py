from qaos.commands.about import execute as about
from qaos.commands.agents import execute as agents
from qaos.commands.bootstrap import execute as bootstrap
from qaos.commands.council import execute as council
from qaos.commands.doctor import execute as doctor
from qaos.commands.run import execute as run
from qaos.commands.status import execute as status
from qaos.commands.version import execute as version

COMMANDS = {
    "about": about,
    "agents": agents,
    "bootstrap": bootstrap,
    "council": council,
    "doctor": doctor,
    "run": run,
    "status": status,
    "version": version,
}
