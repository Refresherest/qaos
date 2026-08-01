from qaos.commands.about import execute as about
from qaos.bootstrap import execute as bootstrap
from qaos.commands.version import execute as version
from qaos.commands.doctor import execute as doctor

COMMANDS = {
    "about": about,
    "bootstrap": bootstrap,
    "doctor": doctor,
    "version": version,
}