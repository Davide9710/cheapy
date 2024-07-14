from supabase import Client

class Item:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

    def save_to_db(self, supabase: Client):
        response = supabase.table("item").insert({
            "name": self.name,
            "description": self.description,
            "price": self.price
        }).execute()
        
        if response.status_code != 201:
            raise Exception(f"Failed to insert item: {response.status_code}")

# Usage example:
# supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
# new_item = Item("Book", "A great novel", 19.99)
# new_item.save_to_db(supabase)