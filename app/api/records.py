from flask import Blueprint, request, jsonify, session
from app.services.records import (
    create_record,
    get_records,
    get_record_by_id,
    update_record,
    delete_record,
    get_record_statistics
)
from datetime import datetime

records_bp = Blueprint('records', __name__)

def check_auth():
    if 'user_id' not in session:
        return None
    return session['user_id']

@records_bp.route('/create', methods=['POST'])
def create():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    title = data.get('title', '').strip()
    category = data.get('category', '').strip()
    value = data.get('value')
    timestamp = data.get('timestamp')
    metadata = data.get('metadata', {})

    if not title or not category or value is None:
        return jsonify({'error': 'Title, category, and value are required'}), 400

    try:
        value = float(value)
    except (ValueError, TypeError):
        return jsonify({'error': 'Value must be a number'}), 400

    if timestamp:
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            timestamp = None

    record = create_record(user_id, title, category, value, timestamp, metadata)

    if record:
        return jsonify({'message': 'Record created', 'record': record}), 201
    else:
        return jsonify({'error': 'Failed to create record'}), 500

@records_bp.route('/list', methods=['GET'])
def list_records():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        start_date = end_date = None

    records = get_records(user_id, category, start_date, end_date)

    return jsonify({'records': records}), 200

@records_bp.route('/<record_id>', methods=['GET'])
def get_record(record_id):
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    record = get_record_by_id(record_id, user_id)

    if record:
        return jsonify(record), 200
    else:
        return jsonify({'error': 'Record not found'}), 404

@records_bp.route('/<record_id>', methods=['PUT'])
def update(record_id):
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json()
    title = data.get('title')
    category = data.get('category')
    value = data.get('value')
    timestamp = data.get('timestamp')
    metadata = data.get('metadata')

    if value is not None:
        try:
            value = float(value)
        except (ValueError, TypeError):
            return jsonify({'error': 'Value must be a number'}), 400

    if timestamp:
        try:
            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            timestamp = None

    record = update_record(record_id, user_id, title, category, value, timestamp, metadata)

    if record:
        return jsonify({'message': 'Record updated', 'record': record}), 200
    else:
        return jsonify({'error': 'Record not found or update failed'}), 404

@records_bp.route('/<record_id>', methods=['DELETE'])
def delete(record_id):
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    success = delete_record(record_id, user_id)

    if success:
        return jsonify({'message': 'Record deleted'}), 200
    else:
        return jsonify({'error': 'Record not found or deletion failed'}), 404

@records_bp.route('/statistics', methods=['GET'])
def statistics():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        start_date = end_date = None

    stats = get_record_statistics(user_id, category, start_date, end_date)

    return jsonify(stats), 200
