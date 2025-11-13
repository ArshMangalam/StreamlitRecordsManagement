from flask import Blueprint, request, jsonify, session
from app.services.jobs import (
    fetch_external_data,
    get_last_job_run,
    get_job_history,
    start_scheduler
)

jobs_bp = Blueprint('jobs', __name__)

def check_auth():
    if 'user_id' not in session:
        return None
    return session['user_id']

@jobs_bp.route('/run', methods=['POST'])
def run_job():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    import os
    external_api_url = os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com/posts")

    result = fetch_external_data(external_api_url)

    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 500

@jobs_bp.route('/last-run', methods=['GET'])
def last_run():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    run = get_last_job_run()

    if run:
        return jsonify(run), 200
    else:
        return jsonify({'message': 'No job runs yet'}), 200

@jobs_bp.route('/history', methods=['GET'])
def history():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    limit = request.args.get('limit', 20, type=int)
    job_history = get_job_history(limit)

    return jsonify({'history': job_history}), 200

@jobs_bp.route('/config', methods=['GET'])
def config():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    import os
    return jsonify({
        'external_api_url': os.getenv("EXTERNAL_API_URL", "https://jsonplaceholder.typicode.com/posts"),
        'job_interval_min': int(os.getenv("JOB_INTERVAL_MIN", "5"))
    }), 200

@jobs_bp.route('/start-scheduler', methods=['POST'])
def start_bg_scheduler():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        start_scheduler()
        return jsonify({'message': 'Background scheduler started'}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to start scheduler: {str(e)}'}), 500
