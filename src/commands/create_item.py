# Command to initiate the item creation process
class CreateItemCommand:
    def execute(self, user, args):
        user.state = 'asking_item_name'
        return "Let's create a new item. What's the name of the item?"