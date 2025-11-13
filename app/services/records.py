from typing import List, Optional, Dict
from datetime import datetime
from app.models import get_supabase_client

def create_record(user_id: str, title: str, category: str, value: float, timestamp: datetime = None, metadata: dict = None) -> Optional[Dict]:
    try:
        client = get_supabase_client()

        record_data = {
            'user_id': user_id,
            'title': title,
            'category': category,
            'value': value,
            'timestamp': timestamp.isoformat() if timestamp else datetime.now().isoformat(),
            'metadata': metadata or {}
        }

        response = client.table('records').insert(record_data).execute()

        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Create record error: {e}")
        return None

def get_records(user_id: str, category: str = None, start_date: datetime = None, end_date: datetime = None) -> List[Dict]:
    try:
        client = get_supabase_client()

        query = client.table('records').select('*').eq('user_id', user_id)

        if category:
            query = query.eq('category', category)

        if start_date:
            query = query.gte('timestamp', start_date.isoformat())

        if end_date:
            query = query.lte('timestamp', end_date.isoformat())

        response = query.order('timestamp', desc=True).execute()

        return response.data if response.data else []
    except Exception as e:
        print(f"Get records error: {e}")
        return []

def get_record_by_id(record_id: str, user_id: str) -> Optional[Dict]:
    try:
        client = get_supabase_client()

        response = client.table('records').select('*').eq('id', record_id).eq('user_id', user_id).maybeSingle().execute()

        return response.data
    except Exception as e:
        print(f"Get record error: {e}")
        return None

def update_record(record_id: str, user_id: str, title: str = None, category: str = None, value: float = None, timestamp: datetime = None, metadata: dict = None) -> Optional[Dict]:
    try:
        client = get_supabase_client()

        update_data = {'updated_at': datetime.now().isoformat()}

        if title is not None:
            update_data['title'] = title
        if category is not None:
            update_data['category'] = category
        if value is not None:
            update_data['value'] = value
        if timestamp is not None:
            update_data['timestamp'] = timestamp.isoformat()
        if metadata is not None:
            update_data['metadata'] = metadata

        response = client.table('records').update(update_data).eq('id', record_id).eq('user_id', user_id).execute()

        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Update record error: {e}")
        return None

def delete_record(record_id: str, user_id: str) -> bool:
    try:
        client = get_supabase_client()

        response = client.table('records').delete().eq('id', record_id).eq('user_id', user_id).execute()

        return True
    except Exception as e:
        print(f"Delete record error: {e}")
        return False

def get_record_statistics(user_id: str, category: str = None, start_date: datetime = None, end_date: datetime = None) -> Dict:
    records = get_records(user_id, category, start_date, end_date)

    if not records:
        return {
            'count': 0,
            'sum': 0,
            'average': 0,
            'min': 0,
            'max': 0
        }

    values = [float(r['value']) for r in records]

    return {
        'count': len(records),
        'sum': sum(values),
        'average': sum(values) / len(values),
        'min': min(values),
        'max': max(values)
    }
