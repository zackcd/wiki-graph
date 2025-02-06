from unittest.mock import Mock
import pytest
from flask import Flask

from routes.category_routes import bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.category_service = Mock()
    app.register_blueprint(bp)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_process_category_success(client, app):
    # Arrange
    mock_result = {
        "message": "Graph generated and persisted successfully",
        "stats": {"nodes": 5, "edges": 10},
        "graph_data": {"nodes": [], "edges": []}
    }
    app.category_service.process_category.return_value = mock_result

    # Act
    response = client.get('/category/Python')

    # Assert
    assert response.status_code == 200
    assert response.json == mock_result
    app.category_service.process_category.assert_called_once_with('Python')

def test_process_category_not_found(client, app):
    # Arrange
    app.category_service.process_category.side_effect = ValueError("No pages found")

    # Act
    response = client.get('/category/NonExistentCategory')

    # Assert
    assert response.status_code == 404
    assert "error" in response.json

def test_process_category_error(client, app):
    # Arrange
    app.category_service.process_category.side_effect = Exception("Database error")

    # Act
    response = client.get('/category/Python')

    # Assert
    assert response.status_code == 500
    assert "error" in response.json 