

import os
from supabase import create_client, Client

def get_supabase() -> Client:
    url = os.getenv("SUPABASE_URL", "https://your-project-id.supabase.co")
    key = os.getenv("SUPABASE_KEY", "your-anon-or-service-key")
    return create_client(url, key)
