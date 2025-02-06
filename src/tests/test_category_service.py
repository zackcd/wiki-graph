import pytest
from unittest.mock import Mock, patch
from services.category_service import CategoryService

@pytest.fixture
def wikipedia_mock():
    return Mock()

@pytest.fixture
def graph_db_mock():
    return Mock()

@pytest.fixture
def service(wikipedia_mock, graph_db_mock):
    return CategoryService(wikipedia_mock, graph_db_mock)

def test_process_category_success(service, wikipedia_mock, graph_db_mock):
    # Arrange
    wikipedia_mock.fetch_category_pages.return_value = ["Page1", "Page2"]
    wikipedia_mock.fetch_page_details.return_value = {
        "title": "Page1",
        "categories": ["Category:Test"],
        "links": ["Page2"]
    }

    # Act
    result = service.process_category("Test")

    # Assert
    assert "message" in result
    assert "stats" in result
    assert "graph_data" in result
    wikipedia_mock.fetch_category_pages.assert_called_once_with("Test", limit=10)
    graph_db_mock.load_graph.assert_called_once()
    graph_db_mock.close.assert_called_once()

def test_process_category_no_pages(service, wikipedia_mock):
    # Arrange
    wikipedia_mock.fetch_category_pages.return_value = []

    # Act/Assert
    with pytest.raises(ValueError, match="No pages found in category 'Test'"):
        service.process_category("Test")

def test_fetch_page_details(service, wikipedia_mock):
    # Arrange
    page_titles = ["Page1", "Page2"]
    wikipedia_mock.fetch_page_details.return_value = {
        "title": "Page1",
        "categories": ["Category:Test"],
        "links": ["Page2"]
    }

    # Act
    result = service._fetch_page_details(page_titles)

    # Assert
    assert len(result) == 2
    assert wikipedia_mock.fetch_page_details.call_count == 2 