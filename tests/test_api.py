import pytest
from unittest.mock import Mock, patch
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_supabase():
    with patch('app.models.get_supabase_client') as mock:
        yield mock

def test_auth_register(client, mock_supabase):
    mock_client = Mock()
    mock_response = Mock()
    mock_response.data = [{
        'id': 'test-id',
        'email': 'test@example.com',
        'is_guest': False
    }]

    mock_client.table.return_value.insert.return_value.execute.return_value = mock_response
    mock_supabase.return_value = mock_client

    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

    assert response.status_code == 201
    assert response.json['user']['email'] == 'test@example.com'

def test_auth_register_missing_fields(client):
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com'
    })

    assert response.status_code == 400
    assert 'required' in response.json['error'].lower()

def test_records_create(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'test-user-id'

    with patch('app.services.records.get_supabase_client') as mock:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [{
            'id': 'record-id',
            'title': 'Test Record',
            'category': 'Test',
            'value': 100.0,
            'user_id': 'test-user-id'
        }]

        mock_client.table.return_value.insert.return_value.execute.return_value = mock_response
        mock.return_value = mock_client

        response = client.post('/api/records/create', json={
            'title': 'Test Record',
            'category': 'Test',
            'value': 100.0
        })

        assert response.status_code == 201
        assert response.json['record']['title'] == 'Test Record'

def test_records_list_unauthorized(client):
    response = client.get('/api/records/list')
    assert response.status_code == 401

def test_records_statistics(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'test-user-id'

    with patch('app.services.records.get_supabase_client') as mock:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            {'value': 100},
            {'value': 200},
            {'value': 300}
        ]

        mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response
        mock.return_value = mock_client

        response = client.get('/api/records/statistics')

        assert response.status_code == 200
        assert response.json['count'] == 3
        assert response.json['sum'] == 600

def test_reports_summary(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'test-user-id'

    with patch('app.services.records.get_supabase_client') as mock:
        mock_client = Mock()
        mock_response = Mock()
        mock_response.data = [
            {'value': 100},
            {'value': 200}
        ]

        mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response
        mock.return_value = mock_client

        response = client.get('/api/reports/summary')

        assert response.status_code == 200
        assert 'statistics' in response.json

def test_jobs_config(client):
    with client.session_transaction() as sess:
        sess['user_id'] = 'test-user-id'

    response = client.get('/api/jobs/config')

    assert response.status_code == 200
    assert 'external_api_url' in response.json
    assert 'job_interval_min' in response.json
