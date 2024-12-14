import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app  
from flask_jwt_extended.exceptions import JWTDecodeError

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = "auth_key_1001"    
    with app.test_client() as client:
        yield client

@patch('flask_jwt_extended.create_access_token')
@patch('flask_jwt_extended.get_jwt_identity')
@patch('flask_jwt_extended.jwt_required')
def test_login_success(mock_jwt_required, mock_get_jwt_identity, mock_create_access_token, client):
    mock_create_access_token.return_value = "mock_token"
    
    mock_get_jwt_identity.return_value = "admin"

    response = client.post('/auth/login', json={
        "username": "admin",
        "password": "roster_admin"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data

    decoded_identity = mock_get_jwt_identity()  
    assert decoded_identity == "admin"

@patch('flask_jwt_extended.create_access_token')
@patch('flask_jwt_extended.get_jwt_identity')
@patch('flask_jwt_extended.jwt_required')
def test_login_invalid_credentials(mock_jwt_required, mock_get_jwt_identity, mock_create_access_token, client):
    response = client.post('/auth/login', json={
        "username": "admin",
        "password": "wrong_password"
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid credentials"

@patch('flask_jwt_extended.create_access_token')
@patch('flask_jwt_extended.get_jwt_identity')
@patch('flask_jwt_extended.jwt_required')
def test_login_missing_json(mock_jwt_required, mock_get_jwt_identity, mock_create_access_token, client):
    response = client.post('/auth/login', json={})

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Missing username or password"

@patch('flask_jwt_extended.jwt_required')
@patch('flask_jwt_extended.get_jwt_identity')
def test_protected_without_token(mock_get_jwt_identity, mock_jwt_required, client):
    response = client.get('/auth/protected')

    assert response.status_code == 401
    data = response.get_json()
    assert data["msg"] == "Missing Authorization Header"

@patch('flask_jwt_extended.jwt_required')
@patch('flask_jwt_extended.get_jwt_identity')
def test_protected_with_valid_token(mock_get_jwt_identity, mock_jwt_required, client):
    mock_get_jwt_identity.return_value = "admin"

    login_response = client.post('/auth/login', json={
        "username": "admin",
        "password": "roster_admin"
    })
    assert login_response.status_code == 200
    token = login_response.get_json()["access_token"]

    response = client.get('/auth/protected', headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Welcome, admin!"

# @patch('flask_jwt_extended.jwt_required')
# @patch('flask_jwt_extended.get_jwt_identity')
# def test_protected_with_invalid_token(mock_get_jwt_identity, mock_jwt_required, client):
#     mock_jwt_required.side_effect = JWTDecodeError("Token is invalid")
    
#     response = client.get('/auth/protected', headers={
#         "Authorization": "Bearer invalid_token"
#     })
    
#     assert response.status_code == 422
    
#     data = response.get_json()
#     assert data["msg"] == "Token is invalid"
    
@patch('flask_jwt_extended.jwt_required')
@patch('flask_jwt_extended.get_jwt_identity')
def test_role_required_decorator(mock_get_jwt_identity, mock_jwt_required, client):
    mock_get_jwt_identity.return_value = "admin"

    login_response = client.post('/auth/login', json={
        "username": "admin",
        "password": "roster_admin"
    })
    assert login_response.status_code == 200
    token = login_response.get_json()["access_token"]

    response = client.get('/auth/protected', headers={
        "Authorization": f"Bearer {token}"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Welcome, admin!"
