import pytest
from datetime import datetime
from app.services.reports import generate_csv, generate_excel, generate_pdf_summary

@pytest.fixture
def sample_records():
    return [
        {
            'id': '1',
            'title': 'Record 1',
            'category': 'Sales',
            'value': 100.50,
            'timestamp': datetime.now().isoformat(),
            'metadata': {'source': 'manual'}
        },
        {
            'id': '2',
            'title': 'Record 2',
            'category': 'Marketing',
            'value': 250.75,
            'timestamp': datetime.now().isoformat(),
            'metadata': {'source': 'import'}
        }
    ]

@pytest.fixture
def sample_statistics():
    return {
        'count': 10,
        'sum': 1500.0,
        'average': 150.0,
        'min': 50.0,
        'max': 300.0
    }

def test_generate_csv_with_records(sample_records):
    result = generate_csv(sample_records)

    assert isinstance(result, bytes)
    assert b'Record 1' in result
    assert b'Record 2' in result
    assert b'Sales' in result
    assert b'Marketing' in result

def test_generate_csv_empty_records():
    result = generate_csv([])

    assert isinstance(result, bytes)
    assert b'id' in result
    assert b'title' in result
    assert b'category' in result

def test_generate_excel_with_records(sample_records):
    result = generate_excel(sample_records)

    assert isinstance(result, bytes)
    assert len(result) > 0

def test_generate_excel_empty_records():
    result = generate_excel([])

    assert isinstance(result, bytes)
    assert len(result) > 0

def test_generate_pdf_summary_with_records(sample_records, sample_statistics):
    result = generate_pdf_summary(sample_records, sample_statistics)

    assert isinstance(result, bytes)
    assert len(result) > 0
    assert result[:4] == b'%PDF'

def test_generate_pdf_summary_empty_records(sample_statistics):
    result = generate_pdf_summary([], sample_statistics)

    assert isinstance(result, bytes)
    assert len(result) > 0
    assert result[:4] == b'%PDF'

def test_csv_contains_all_columns(sample_records):
    result = generate_csv(sample_records)
    result_str = result.decode('utf-8')

    assert 'id' in result_str
    assert 'title' in result_str
    assert 'category' in result_str
    assert 'value' in result_str
    assert 'timestamp' in result_str
    assert 'metadata' in result_str
