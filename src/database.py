from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_ANON_KEY
from .models import Item

# For reference check https://supabase.com/docs/reference/python/insert

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def save_item_to_db(item: Item):
    try:
        supabase.table("item").insert(
            {
                "name": item.name, 
                "category": item.category,
                "price": item.price,
                "description": item.description,
            }
        ).execute()
    except ValueError as e:
        raise Exception(f"Failed to insert item: {str(e)}")