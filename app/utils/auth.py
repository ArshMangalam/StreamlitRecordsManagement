import bcrypt
import uuid
from typing import Optional, Dict
from datetime import datetime
from app.utils.database import get_supabase_client

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(email: str, password: str, is_guest: bool = False) -> Optional[Dict]:
    try:
        client = get_supabase_client()
        password_hash = hash_password(password)

        response = client.table('users').insert({
            'email': email,
            'password_hash': password_hash,
            'is_guest': is_guest
        }).execute()

        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Registration error: {e}")
        return None

def login_user(email: str, password: str) -> Optional[Dict]:
    try:
        client = get_supabase_client()

        response = client.table('users').select('*').eq('email', email).maybeSingle().execute()

        if response.data:
            user = response.data
            if verify_password(password, user['password_hash']):
                return user

        return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def create_guest_user() -> Optional[Dict]:
    guest_email = f"guest_{uuid.uuid4().hex[:8]}@guest.local"
    guest_password = uuid.uuid4().hex
    return register_user(guest_email, guest_password, is_guest=True)
