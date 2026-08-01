from qaos.commands.version import execute as version
from qaos.commands.doctor import execute as doctor
from qaos.bootstrap import execute as bootstrap

COMMANDS = {
    "version": version,
    "doctor": doctor,
    "bootstrap": bootstrap,
}