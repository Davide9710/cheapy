# Command to initiate the item creation process
class CreateItemCommand:
    def execute(self, user):
        user.state = 'asking_item_name'
        print("Let's create a new item. What's the name of the item?")
        return "Let's create a new item. What's the name of the item?"