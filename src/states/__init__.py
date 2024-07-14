from .initial import InitialState
from .awaiting_input import AwaitingInputState

states = {
    'initial': InitialState(),
    'awaiting_input': AwaitingInputState(),
}

def get_state(name):
    return states.get(name, states['initial'])