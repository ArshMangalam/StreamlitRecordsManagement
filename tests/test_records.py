import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from app.services.records import create_record, get_records, update_record, delete_record, get_record_statistics

@pytest.fixture
def mock_supabase_client():
    with patch('app.services.records.get_supabase_client') as mock:
        client = Mock()
        mock.return_value = client
        yield client

def test_create_record_success(mock_supabase_client):
    mock_response = Mock()
    mock_response.data = [{
        'id': 'test-id',
        'user_id': 'user-123',
        'title': 'Test Record',
        'category': 'Test',
        'value': 100.0,
        'timestamp': datetime.now().isoformat(),
        'metadata': {}
    }]

    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response

    result = create_record('user-123', 'Test Record', 'Test', 100.0)

    assert result is not None
    assert result['title'] == 'Test Record'
    assert result['category'] == 'Test'
    assert result['value'] == 100.0

def test_create_record_with_metadata(mock_supabase_client):
    metadata = {'key': 'value', 'number': 42}

    mock_response = Mock()
    mock_response.data = [{
        'id': 'test-id',
        'user_id': 'user-123',
        'title': 'Test Record',
        'category': 'Test',
        'value': 100.0,
        'timestamp': datetime.now().isoformat(),
        'metadata': metadata
    }]

    mock_supabase_client.table.return_value.insert.return_value.execute.return_value = mock_response

    result = create_record('user-123', 'Test Record', 'Test', 100.0, metadata=metadata)

    assert result is not None
    assert result['metadata'] == metadata

def test_get_records_no_filters(mock_supabase_client):
    mock_response = Mock()
    mock_response.data = [
        {'id': '1', 'title': 'Record 1', 'value': 100},
        {'id': '2', 'title': 'Record 2', 'value': 200}
    ]

    mock_supabase_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response

    result = get_records('user-123')

    assert len(result) == 2
    assert result[0]['title'] == 'Record 1'

def test_update_record_success(mock_supabase_client):
    mock_response = Mock()
    mock_response.data = [{
        'id': 'record-123',
        'title': 'Updated Title',
        'value': 150.0
    }]

    mock_supabase_client.table.return_value.update.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

    result = update_record('record-123', 'user-123', title='Updated Title', value=150.0)

    assert result is not None
    assert result['title'] == 'Updated Title'

def test_delete_record_success(mock_supabase_client):
    mock_response = Mock()
    mock_response.data = [{'id': 'record-123'}]

    mock_supabase_client.table.return_value.delete.return_value.eq.return_value.eq.return_value.execute.return_value = mock_response

    result = delete_record('record-123', 'user-123')

    assert result is True

def test_get_record_statistics_empty():
    with patch('app.services.records.get_records') as mock_get:
        mock_get.return_value = []

        result = get_record_statistics('user-123')

        assert result['count'] == 0
        assert result['sum'] == 0
        assert result['average'] == 0

def test_get_record_statistics_with_data():
    with patch('app.services.records.get_records') as mock_get:
        mock_get.return_value = [
            {'value': 100},
            {'value': 200},
            {'value': 300}
        ]

        result = get_record_statistics('user-123')

        assert result['count'] == 3
        assert result['sum'] == 600
        assert result['average'] == 200
        assert result['min'] == 100
        assert result['max'] == 300
