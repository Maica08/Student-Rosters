import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'test'
    app.config['MYSQL_PASSWORD'] = 'test'
    app.config['MYSQL_DB'] = 'test_db'
    with app.test_client() as client:
        yield client
