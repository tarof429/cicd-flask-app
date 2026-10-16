import pytest
import json

from app import create_app

def test_index_page():
    app = create_app(mode='test')

    client = app.test_client()

    """Test that the health endpoint returns 200"""
    response = client.get('/')

    assert response.status_code == 200

def test_list_events():
    app = create_app(mode='test')

    client = app.test_client()

    """Test that the health endpoint returns 200"""
    response = client.get('/list_events')

    assert response.status_code == 200