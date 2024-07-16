from ..database import save_item_to_db

# States for the item creation process
class AskingItemNameState:
    def handle(self, user, message):
        user.temp_item = {'name': message}
        return "Great! Now, what category does this item belong to?", 'asking_item_category'

class AskingItemCategoryState:
    def handle(self, user, message):
        user.temp_item['category'] = message
        return "Excellent. What's the price of the item?", 'asking_item_price'

class AskingItemPriceState:
    def handle(self, user, message):
        try:
            price = float(message)
            user.temp_item['price'] = price
            return f"Got it. Can you provide a brief description of the item?", 'asking_item_description'
        except ValueError:
            return "Please enter a valid number for the price.", 'asking_item_price'

class AskingItemDescriptionState:
    def handle(self, user, message):
        user.temp_item['description'] = message
        return "Thanks! Here's a summary of the item. Is this correct? (Yes/No)\n" + \
               f"Name: {user.temp_item['name']}\n" + \
               f"Category: {user.temp_item['category']}\n" + \
               f"Price: ${user.temp_item['price']:.2f}\n" + \
               f"Description: {user.temp_item['description']}", 'confirming_item'

class ConfirmingItemState:
    def handle(self, user, message):
        if message.lower() == 'yes':
            # Save the item to the database
            print("user.temp_item")
            print(user.temp_item)

            item_id = save_item_to_db(user.temp_item)
            user.temp_item = None  # Clear the temporary item
            return f"Great! Your item has been created with ID: {item_id}. What would you like to do next?", 'main_menu'
        elif message.lower() == 'no':
            user.temp_item = None  # Clear the temporary item
            return "No problem. Let's start over. What's the name of the item?", 'asking_item_name'
        else:
            return "Please answer with 'Yes' or 'No'.", 'confirming_item'