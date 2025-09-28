import pytest
from app import create_app, db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_index(client):
    """Test index endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert 'SoportePlus Backend API' in data['message']