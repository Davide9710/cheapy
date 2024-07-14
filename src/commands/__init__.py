from .start import StartCommand
from .help import HelpCommand

commands = {
    'start': StartCommand(),
    'help': HelpCommand(),
}

def get_command(name):
    return commands.get(name, commands['help'])