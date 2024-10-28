from ..models import Item

# Command to initiate the item creation process
class SearchItemCommand:
    def execute(self, user):
        user.state = 'asking_item_name'
        user.temp_item = Item(name='', category='', price=0.0, description='')
        return "Let's create a new item. What's the name of the item?"