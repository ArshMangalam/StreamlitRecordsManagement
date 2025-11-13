import os
import requests
from datetime import datetime
from typing import Optional, Dict, List
from app.models import get_supabase_client
from apscheduler.schedulers.background import BackgroundScheduler

_scheduler: Optional[BackgroundScheduler] = None

def fetch_external_data(url: str) -> Dict:
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        client = get_supabase_client()

        result = client.table('background_data').insert({
            'source_url': url,
            'data': data if isinstance(data, dict) else {'items': data},
            'fetched_at': datetime.now().isoformat(),
            'status': 'success',
            'error_message': None
        }).execute()

        return {
            'success': True,
            'message': f'Successfully fetched data from {url}',
            'record_count': len(data) if isinstance(data, list) else 1
        }

    except Exception as e:
        try:
            client = get_supabase_client()
            client.table('background_data').insert({
                'source_url': url,
                'data': {},
                'fetched_at': datetime.now().isoformat(),
                'status': 'error',
                'error_message': str(e)
            }).execute()
        except:
            pass

        return {
            'success': False,
            'message': f'Error fetching data: {str(e)}'
        }

def get_last_job_run() -> Optional[Dict]:
    try:
        client = get_supabase_client()

        response = client.table('background_data').select('*').order('fetched_at', desc=True).limit(1).execute()

        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting last job run: {e}")
        return None

def get_job_history(limit: int = 10) -> List[Dict]:
    try:
        client = get_supabase_client()

        response = client.table('background_data').select('*').order('fetched_at', desc=True).limit(limit).execute()

        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting job history: {e}")
        return []

def start_scheduler():
    global _scheduler

    if _scheduler is not None and _scheduler.running:
        return

    _scheduler = BackgroundScheduler()
    external_api_url = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com/posts")
    job_interval = int(os.getenv("JOB_INTERVAL_MIN", "5"))

    _scheduler.add_job(
        func=lambda: fetch_external_data(external_api_url),
        trigger="interval",
        minutes=job_interval,
        id="fetch_external_data",
        name="Fetch External Data",
        replace_existing=True
    )

    _scheduler.start()

def stop_scheduler():
    global _scheduler

    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown()
        _scheduler = None
