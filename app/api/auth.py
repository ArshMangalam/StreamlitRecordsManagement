from flask import Blueprint, request, jsonify, session
from app.services.auth import (
    register_user,
    login_user,
    create_guest_user,
    get_user_by_id
)
import uuid

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    user = register_user(email, password)

    if user:
        return jsonify({'message': 'Registration successful', 'user': user}), 201
    else:
        return jsonify({'error': 'Registration failed. Email might already exist.'}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400

    user = login_user(email, password)

    if user:
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/guest', methods=['POST'])
def guest():
    user = create_guest_user()

    if user:
        session['user_id'] = user['id']
        session['user_email'] = user['email']
        return jsonify({'message': 'Guest account created', 'user': user}), 201
    else:
        return jsonify({'error': 'Failed to create guest account'}), 500

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    user = get_user_by_id(user_id)

    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
