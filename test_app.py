import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  
    app.config['MYSQL_HOST'] = 'mock_host'
    app.config['MYSQL_USER'] = 'mock_user'
    app.config['MYSQL_PASSWORD'] = 'mock_password'
    app.config['MYSQL_DB'] = 'mock_db'

    with app.app_context():  
        with app.test_client() as client:
            yield client

# Test for students
@patch('app.mysql.connection')
def test_get_students_api(mock_connection, client):
    # Mock cursor and its methods
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'idstudents': 1, 'firstname': 'John', 'lastname': 'Doe', 'birthdate': '2000-01-01', 'gender': 'M'}
    ]
    mock_cursor.description = (
        ('idstudents',), ('firstname',), ('lastname',), ('birthdate',), ('gender',)
    )

    response = client.get('/api/students')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == [
        {'idstudents': 1, 'firstname': 'John', 'lastname': 'Doe', 'birthdate': '2000-01-01', 'gender': 'M'}
    ]

@patch('app.mysql.connection')
def test_add_students(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    

    response = client.post(
        '/api/students',
        json={
            'firstname': 'Jane',
            'middlename': 'Q',
            'lastname': 'Smith',
            'birthdate': '1999-12-31',
            'gender': 'F'
        }
    )

    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data created successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_update_students(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.put(
        '/api/students/1',
        json={
            'firstname': 'Jane',
            'lastname': 'Doe',
            'birthdate': '1995-06-15',
            'gender': 'F'
        }
    )

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data updated successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_delete_student(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    response = client.delete('/api/students/1')

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_students_missing_fields(mock_connection, client):
    response = client.post(
        '/api/students',
        json={
            'firstname': 'Jane',
            'lastname': 'Smith'
        }
    )

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert 'error' in data
    assert data['message'] == "'birthdate' is required"

@patch('app.mysql.connection')
def test_get_students_no_data(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    response = client.get('/api/students')

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'data not found'
