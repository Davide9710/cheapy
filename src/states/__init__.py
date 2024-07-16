from .initial import InitialState
from .awaiting_input import AwaitingInputState
from .create_item_states import *

states = {
    'initial': InitialState(),
    'awaiting_input': AwaitingInputState(),
    'asking_item_name': AskingItemNameState(),
    'asking_item_category': AskingItemCategoryState(),
    'asking_item_price': AskingItemPriceState(),
    'confirming_item': ConfirmingItemState()
}

def get_state(name):
    return states.get(name, states['initial'])