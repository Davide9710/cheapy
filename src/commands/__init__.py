from start import StartCommand
from help import HelpCommand
from create_item import CreateItemCommand

commands = {
    'start': StartCommand(),
    'help': HelpCommand(),
    'create-item': CreateItemCommand()
}

def get_command(name):
    return commands.get(name, commands['help'])