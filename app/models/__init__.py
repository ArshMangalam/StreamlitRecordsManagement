import os
from supabase import create_client, Client
from typing import Optional

_supabase_client: Optional[Client] = None

def get_supabase_client() -> Client:
    global _supabase_client

    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")

        _supabase_client = create_client(url, key)

    return _supabase_client
