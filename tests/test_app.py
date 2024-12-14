import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import create_access_token
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True  
    app.config['MYSQL_HOST'] = 'mock_host'
    app.config['MYSQL_USER'] = 'mock_user'
    app.config['MYSQL_PASSWORD'] = 'mock_password'
    app.config['MYSQL_DB'] = 'mock_db'
    app.config['JWT_SECRET_KEY'] = "auth_key_1001"  

    with patch('app.mysql') as mock_mysql:
        mock_connection = MagicMock()
        mock_mysql.connection = mock_connection
        yield app.test_client()

def generate_token(role):
    """Helper function to generate a JWT token with the specified role."""
    with app.app_context():
        return create_access_token(identity='test_user', additional_claims={'role': role})

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

    token = generate_token('admin') 
    response = client.get('/api/students', headers={'Authorization': f'Bearer {token}'})
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
    
    token = generate_token('admin') 
    response = client.post(
        '/api/students',
        json={
            'firstname': 'Jane',
            'middlename': 'Kelly',
            'lastname': 'Smith',
            'birthdate': '1999-12-31',
            'gender': 'F'
        },
        headers={'Authorization': f'Bearer {token}'}
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
    
    token = generate_token('admin') 
    response = client.put(
        '/api/students/1',
        json={
            'firstname': 'Jane',
            'lastname': 'Doe',
            'birthdate': '1995-06-15',
            'gender': 'Female'
        },
        headers={'Authorization': f'Bearer {token}'}
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
    token = generate_token('admin') 

    response = client.delete('/api/students/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_students_missing_fields(mock_connection, client):
    token = generate_token('admin') 
    response = client.post(
        '/api/students',
        json={
            'firstname': 'Jane',
            'lastname': 'Smith'
        },
        headers={'Authorization': f'Bearer {token}'}
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
    token = generate_token('admin') 

    response = client.get('/api/students', headers={'Authorization': f'Bearer {token}'})

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

    token = generate_token('admin') 
    response = client.get('/api/teachers', headers={'Authorization': f'Bearer {token}'})
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
    
    token = generate_token('admin') 
    response = client.post(
        '/api/students',
        json={
            'firstname': 'Jane',
            'middlename': 'Kelly',
            'lastname': 'Smith',
            'birthdate': '1999-12-31',
            'gender': 'Female'
        },
        headers={'Authorization': f'Bearer {token}'}
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
    
    token = generate_token('admin') 
    response = client.put(
        '/api/teachers/1',
        json={
            'firstname': 'Henry',
            'lastname': 'Doer',
            'birthdate': '1990-06-10',
            'gender': 'Male'
        },
        headers={'Authorization': f'Bearer {token}'}
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

    token = generate_token('admin') 
    response = client.delete('/api/teachers/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_teachers_missing_fields(mock_connection, client):
    token = generate_token('admin') 
    response = client.post(
        '/api/teachers',
        json={
            'firstname': 'Roy',
            'lastname': 'Smith'
        },
        headers={'Authorization': f'Bearer {token}'}
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

    token = generate_token('admin') 
    response = client.get('/api/teachers', headers={'Authorization': f'Bearer {token}'})

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

    token = generate_token('admin') 
    response = client.get('/api/classes', headers={'Authorization': f'Bearer {token}'})
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
    
    token = generate_token('admin') 
    response = client.post(
        '/api/classes',
        json={
            'description': 'Basic Calculus',
            'idroom': 1,
            'idcourse': 26
        }, 
        headers={'Authorization': f'Bearer {token}'}
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
    
    token = generate_token('admin')
    response = client.put(
        '/api/classes/1',
        json={
            'description': 'Math in the Modern World',
            'idroom': 1,
            'idcourse': 25
        },
        headers={'Authorization': f'Bearer {token}'}
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

    token = generate_token('admin')
    response = client.delete('/api/classes/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_classes_missing_fields(mock_connection, client):
    token = generate_token('admin')
    response = client.post(
        '/api/classes',
        json={
            'idroom': 1,
            'idcourse': 25
        },
        headers={'Authorization': f'Bearer {token}'}
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

    token = generate_token('admin')
    response = client.get('/api/classes', headers={'Authorization': f'Bearer {token}'})

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

    token = generate_token('admin')
    response = client.get('/api/rooms', headers={'Authorization': f'Bearer {token}'})
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
    
    token = generate_token('admin')
    response = client.post(
        '/api/rooms',
        json={
            'location': 'Main Building, Room 1',
            'description': 'Meeting room'
        },
        headers={'Authorization': f'Bearer {token}'}
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
    
    token = generate_token('admin')
    response = client.put(
        '/api/rooms/1',
        json={
            'location': 'New Building, Room 2',
            'description': 'Grand hall'
        },
        headers={'Authorization': f'Bearer {token}'}
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

    token = generate_token('admin')
    response = client.delete('/api/rooms/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_rooms_missing_fields(mock_connection, client):
    token = generate_token('admin')
    response = client.post(
        '/api/rooms',
        json={
            'description': 'Grand hall'
        },
        headers={'Authorization': f'Bearer {token}'}
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

    token = generate_token('admin')
    response = client.get('/api/rooms', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'data not found'

# Test for courses
@patch('app.mysql.connection')
def test_get_courses_api(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'idcourses': 1, 'name': 'Modern Literature', 'code': 'EL1'}
    ]
    mock_cursor.description = (
        ('idcourses',), ('name',), ('code',)
    )

    token = generate_token('admin')
    response = client.get('/api/courses', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == [
        {'idcourses': 1, 'name': 'Modern Literature', 'code': 'EL1'}
    ]

@patch('app.mysql.connection')
def test_add_courses(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    token = generate_token('admin')
    response = client.post(
        '/api/courses',
        json={
            'name': 'Western Literature', 
            'code': 'EL101'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data created successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_update_courses(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    token = generate_token('admin')    
    response = client.put(
        '/api/courses/1',
        json={
            'name': 'Western History', 
            'code': 'H101'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data updated successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_delete_course(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    token = generate_token('admin')
    response = client.delete('/api/courses/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_courses_missing_fields(mock_connection, client):
    token = generate_token('admin')
    response = client.post(
        '/api/courses',
        json={
            'name': 'Western Literature', 
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data['error'] == "Bad Request"
    assert data['message'] == "400 Bad Request: 'code' is required"

@patch('app.mysql.connection')
def test_get_courses_no_data(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    token = generate_token('admin')
    response = client.get('/api/courses', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'data not found'

# Test for roster
@patch('app.mysql.connection')
def test_get_roster_api(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'idroster': 1, 'idclass': 1, 'idstudent': 1, 'idteacher': 1, 'class_period': 'Morning'}
    ]
    mock_cursor.description = (
        ('idroster',), ('idclass',), ('idstudent',), ('idteacher',)
    )

    token = generate_token('admin')
    response = client.get('/api/roster', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data == [
        {'idroster': 1, 'idclass': 1, 'idstudent': 1, 'idteacher': 1, 'class_period': 'Morning'}
    ]

@patch('app.mysql.connection')
def test_add_roster(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    token = generate_token('admin')
    response = client.post(
        '/api/roster',
        json={
            'idclass': 1, 
            'idstudent': 2, 
            'idteacher': 3, 
            'class_period': 'Morning'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 201
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data created successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_update_roster(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    token = generate_token('admin')
    response = client.put(
        '/api/roster/1',
        json={
            'idclass': 1, 
            'idstudent': 2, 
            'idteacher': 3, 
            'class_period': 'Afternoon'
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data updated successfully'
    assert data['rows_affected'] == 1

@patch('app.mysql.connection')
def test_delete_roster(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1

    token = generate_token('admin')
    response = client.delete('/api/roster/1', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert data['message'] == 'data deleted successfully'
    assert data['rows_affected'] == 1
    
@patch('app.mysql.connection')
def test_add_roster_missing_fields(mock_connection, client):
    token = generate_token('admin')
    response = client.post(
        '/api/roster',
        json={
            'idclass': 1, 
            'idstudent': 2, 
            'idteacher': 3, 
        },
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert response.is_json
    data = response.get_json()
    assert data['error'] == "Bad Request"
    assert data['message'] == "400 Bad Request: 'class_period' is required"

@patch('app.mysql.connection')
def test_get_roster_no_data(mock_connection, client):
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []

    token = generate_token('admin')
    response = client.get('/api/roster', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert 'message' in data
    assert data['message'] == 'data not found'
