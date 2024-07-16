from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_ANON_KEY
from .models import Item

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def save_item_to_db(item: Item):
    response = supabase.table("item").insert(
        {"name": item.name, 
         "category": item.category,
         "price": item.price,
         "description": item.description, 
         }
    ).execute()
    if response.get('error'):
        raise Exception(f"Failed to insert item: {response['error'].get('message', 'Unknown error')}")