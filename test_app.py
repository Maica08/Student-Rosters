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

    with patch('app.mysql') as mock_mysql:
        mock_connection = MagicMock()
        mock_mysql.connection = mock_connection
        yield app.test_client()
        
# Test for students
@patch('app.mysql.connection')
def test_get_students_api(mock_connection, client):
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
            'middlename': 'Kelly',
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
            'gender': 'Female'
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
    assert data['error'] == "Bad Request"
    assert data['message'] == "400 Bad Request: 'birthdate' is required"

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


# Test for teachers
@patch('app.mysql.connection')
def test_get_teachers_api(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'idteachers': 1, 'firstname': 'John', 'lastname': 'Doe', 'birthdate': '2000-01-01', 'gender': 'M'}
    ]
    mock_cursor.description = (
        ('idteachers',), ('firstname',), ('lastname',), ('birthdate',), ('gender',)
    )

    response = client.get('/api/teachers')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == [
        {'idteachers': 1, 'firstname': 'John', 'lastname': 'Doe', 'birthdate': '2000-01-01', 'gender': 'M'}
    ]

@patch('app.mysql.connection')
def test_add_teachers(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    

    response = client.post(
        '/api/students',
        json={
            'firstname': 'Jane',
            'middlename': 'Kelly',
            'lastname': 'Smith',
            'birthdate': '1999-12-31',
            'gender': 'Female'
        }
    )

    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data created successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_update_teachers(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.put(
        '/api/teachers/1',
        json={
            'firstname': 'Henry',
            'lastname': 'Doer',
            'birthdate': '1990-06-10',
            'gender': 'Male'
        }
    )

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data updated successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_delete_teacher(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    response = client.delete('/api/teachers/1')

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_teachers_missing_fields(mock_connection, client):
    response = client.post(
        '/api/teachers',
        json={
            'firstname': 'Roy',
            'lastname': 'Smith'
        }
    )

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data['error'] == "Bad Request"
    assert data['message'] == "400 Bad Request: 'birthdate' is required"

@patch('app.mysql.connection')
def test_get_teachers_no_data(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    response = client.get('/api/teachers')

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'data not found'
    
# Test for classes
@patch('app.mysql.connection')
def test_get_classes_api(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'idclasses': 1, 'description': 'Algebra basics class', 'idroom': 1, 'idcourse': 1}
    ]
    mock_cursor.description = (
        ('idclasses',), ('description',), ('idroom',), ('idcourse',)
    )

    response = client.get('/api/classes')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == [
        {'idclasses': 1, 'description': 'Algebra basics class', 'idroom': 1, 'idcourse': 1}
    ]

@patch('app.mysql.connection')
def test_add_classes(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    

    response = client.post(
        '/api/classes',
        json={
            'description': 'Basic Calculus',
            'idroom': 1,
            'idcourse': 26
        }
    )

    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data created successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_update_classes(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.put(
        '/api/classes/1',
        json={
            'description': 'Math in the Modern World',
            'idroom': 1,
            'idcourse': 25
        }
    )

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data updated successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_delete_class(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    response = client.delete('/api/classes/1')

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_classes_missing_fields(mock_connection, client):
    response = client.post(
        '/api/classes',
        json={
            'idroom': 1,
            'idcourse': 25
        }
    )

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data['error'] == "Bad Request"
    assert data['message'] == "400 Bad Request: 'description' is required"

@patch('app.mysql.connection')
def test_get_classes_no_data(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    response = client.get('/api/classes')

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'data not found'


# Test for rooms
@patch('app.mysql.connection')
def test_get_rooms_api(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'idrooms': 1, 'location': 'Main Building, Room 2', 'description': 'Conference hall'}
    ]
    mock_cursor.description = (
        ('idrooms',), ('location',), ('description',), ('idcourse',)
    )

    response = client.get('/api/rooms')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == [
        {'idrooms': 1, 'location': 'Main Building, Room 2', 'description': 'Conference hall'}
    ]

@patch('app.mysql.connection')
def test_add_rooms(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    

    response = client.post(
        '/api/rooms',
        json={
            'location': 'Main Building, Room 1',
            'description': 'Meeting room'
        }
    )

    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data created successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_update_rooms(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.put(
        '/api/rooms/1',
        json={
            'location': 'New Building, Room 2',
            'description': 'Grand hall'
        }
    )

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data updated successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_delete_room(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    response = client.delete('/api/rooms/1')

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_rooms_missing_fields(mock_connection, client):
    response = client.post(
        '/api/rooms',
        json={
            'description': 'Grand hall'
        }
    )

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data['error'] == "Bad Request"
    assert data['message'] == "400 Bad Request: 'location' is required"

@patch('app.mysql.connection')
def test_get_rooms_no_data(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    response = client.get('/api/rooms')

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'data not found'


