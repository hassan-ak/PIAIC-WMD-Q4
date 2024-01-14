"""
Module: test_main.py

This module contains test cases for the FastAPI CRUD operations defined in the main.py file.
It utilizes the Pytest framework for testing.

Test Cases:
- Test creating a Todo successfully.
- Test handling validation error when creating a Todo.
- Test handling internal server error when creating a Todo.
- Test getting an empty list of Todos.
- Test getting Todos after creating one.
- Test getting Todos after creating multiple.
- Test handling internal server error when getting Todos.
- Test getting a non-existent Todo.
- Test getting an existing Todo.
- Test handling internal server error when getting a Todo.
- Test deleting an existing Todo.
- Test handling internal server error when deleting a Todo.
- Test handling validation error when updating a Todo.
- Test updating a non-existent Todo.
- Test updating an existing Todo.
- Test handling internal server error when updating a Todo.
"""

import pytest
from fastapi.testclient import TestClient
from main import app, get_db


@pytest.fixture
def test_client():
    """Fixture to provide a FastAPI TestClient for each test case."""
    return TestClient(app)


def test_create_todo_success(test_client):
    """Test creating a Todo successfully."""
    todo_data = {"todo": {"title": "Test Todo", "description": "Test Description"}}
    response = test_client.post("/api/todos", json=todo_data)
    assert response.status_code == 200
    created_todo = response.json()
    id = created_todo["id"]

    # Clean up: Delete the created Todo
    test_client.delete(f"/api/todos/{id}")

    # Assertions
    assert created_todo["id"] is not None
    assert created_todo["title"] == todo_data["todo"]["title"]
    assert created_todo["description"] == todo_data["todo"]["description"]


def test_create_todo_validation_error(test_client):
    """Test handling validation error when creating a Todo."""
    todo_data = {"todo": {"description": "Test Description"}}
    response = test_client.post("/api/todos", json=todo_data)
    assert response.status_code == 422


# Marking the test as expected to fail using xfail
@pytest.mark.xfail
def test_create_todo_internal_server_error(test_client):
    """
    Test the behavior when creating a todo results in an internal server error.

    This test is marked as xfail, meaning it is expected to fail.
    """
    # Define the todo data for the test
    todo_data = {"todo": {"title": "Test Todo", "description": "Test Description"}}

    # Mocking the get_db dependency to raise an exception
    def mock_get_db():
        raise Exception("Mocked exception in get_db")

    # Override the get_db dependency with the mock function
    app.dependency_overrides[get_db] = mock_get_db

    try:
        # Perform the HTTP request to create a todo
        response = test_client.post("/api/todos", json=todo_data)

        # Assert that the response status code is 500 (Internal Server Error)
        assert response.status_code == 500

    finally:
        # Reset the get_db dependency override after the test
        app.dependency_overrides[get_db] = get_db


def test_get_todos_empty(test_client):
    """
    Test the behavior of getting todos when the list is empty.

    This test checks that the response status code is 200 and the returned todos list is empty.
    """
    # Perform the HTTP request to get todos
    response = test_client.get("/api/todos")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Parse the response JSON content into a list of todos
    todos = response.json()

    # Assert that the todos variable is a list
    assert isinstance(todos, list)

    # Assert that the length of the todos list is 0 (empty)
    assert len(todos) == 0


def test_get_todos_after_creation(test_client):
    """
    Test retrieving todos after creating a single todo.

    Parameters:
    - test_client: Test client for making HTTP requests.

    Steps:
    1. Create a test todo using POST request.
    2. Retrieve all todos using GET request.
    3. Delete the created todo.
    4. Assert the response status code is 200.
    5. Assert the response contains a list of todos with the expected structure.
    """
    todo_data = {"todo": {"title": "Test Todo", "description": "Test Description"}}
    response1 = test_client.post("/api/todos", json=todo_data)
    response = test_client.get("/api/todos")
    created_todo = response1.json()
    id = created_todo["id"]
    test_client.delete(f"/api/todos/{id}")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) == 1
    assert "id" in todos[0]
    assert "title" in todos[0]
    assert "description" in todos[0]


def test_get_todos_after_multiple_creation(test_client):
    """
    Test retrieving todos after creating multiple todos.

    Parameters:
    - test_client: Test client for making HTTP requests.

    Steps:
    1. Create two test todos using POST requests.
    2. Retrieve all todos using GET request.
    3. Delete the created todos.
    4. Assert the response status code is 200.
    5. Assert the response contains a list of todos with the expected structure.
    """
    todo_data1 = {"todo": {"title": "Test Todo 1", "description": "Test Description"}}
    todo_data2 = {"todo": {"title": "Test Todo 2", "description": "Test Description"}}
    response1 = test_client.post("/api/todos", json=todo_data1)
    response2 = test_client.post("/api/todos", json=todo_data2)
    response = test_client.get("/api/todos")
    created_todo = response1.json()
    id1 = created_todo["id"]
    created_todo = response2.json()
    id2 = created_todo["id"]
    test_client.delete(f"/api/todos/{id1}")
    test_client.delete(f"/api/todos/{id2}")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)
    assert len(todos) == 2
    assert "id" in todos[0]
    assert "title" in todos[0]
    assert "description" in todos[0]


import pytest


# Test case using pytest.mark.xfail to mark an expected failure
@pytest.mark.xfail
def test_get_todos_internal_server_error(test_client):
    """
    Test case for handling internal server error in get_todos.

    This test simulates a scenario where the `get_db` dependency raises an exception,
    leading to an internal server error (status code 500) when trying to get todos.

    Args:
        test_client: Pytest fixture for testing HTTP clients.
    """

    def mock_get_db():
        raise Exception("Mocked exception in get_db")

    app.dependency_overrides[get_db] = mock_get_db
    try:
        response = test_client.get("/api/todos")
        assert response.status_code == 500
    finally:
        app.dependency_overrides[get_db] = get_db


def test_get_todo_empty(test_client):
    """
    Test case for handling an empty todo request.

    This test checks if the server returns a 404 status code and the expected JSON response
    when attempting to get a todo with an invalid ID.

    Args:
        test_client: Pytest fixture for testing HTTP clients.
    """
    id = 25000
    response = test_client.get(f"/api/todos/{id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_get_todo(test_client):
    """
    Test case for successfully getting a todo.

    This test creates a new todo, retrieves it, and then deletes it. It checks if the server
    returns the expected status code (200) and JSON response for the get todo request.

    Args:
        test_client: Pytest fixture for testing HTTP clients.
    """
    todo_data = {"todo": {"title": "Test Todo", "description": "Test Description"}}
    response = test_client.post("/api/todos", json=todo_data)
    created_todo = response.json()
    id = created_todo["id"]
    response = test_client.get(f"/api/todos/{id}")
    test_client.delete(f"/api/todos/{id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": id,
        "title": "Test Todo",
        "description": "Test Description",
    }


import pytest


# Test for handling internal server error when getting a todo
@pytest.mark.xfail
def test_get_todo_internal_server_error(test_client):
    """
    Test case for handling internal server error when getting a todo.
    Uses a mocked dependency to simulate an exception in get_db.
    Expects the response status code to be 500.
    """

    def mock_get_db():
        raise Exception("Mocked exception in get_db")

    app.dependency_overrides[get_db] = mock_get_db
    try:
        response = test_client.get("/api/todos/{1}")
        assert response.status_code == 500
    finally:
        app.dependency_overrides[get_db] = get_db


# Test for deleting a todo
def test_delete_todo(test_client):
    """
    Test case for deleting a todo.
    Creates a todo, deletes it, and checks if it's not found after deletion.
    Expects the response status code to be 404 for the fetched todo
    and the deleted_todo response to contain a success message.
    """
    todo_data = {"todo": {"title": "Test Todo", "description": "Test Description"}}
    response = test_client.post("/api/todos", json=todo_data)
    created_todo = response.json()
    id = created_todo["id"]
    deleted_todo = test_client.delete(f"/api/todos/{id}")
    fetched_todo = test_client.get(f"/api/todos/{id}")
    assert fetched_todo.status_code == 404
    assert fetched_todo.json() == {"detail": "Todo not found"}
    assert deleted_todo.json() == {"message": "Todo deleted successfully"}


# Test for handling internal server error when deleting a todo
@pytest.mark.xfail
def test_delete_todo_internal_server_error(test_client):
    """
    Test case for handling internal server error when deleting a todo.
    Uses a mocked dependency to simulate an exception in get_db.
    Expects the response status code to be 500.
    """

    def mock_get_db():
        raise Exception("Mocked exception in get_db")

    app.dependency_overrides[get_db] = mock_get_db
    try:
        response = test_client.delete("/api/todos/{1}")
        assert response.status_code == 500
    finally:
        app.dependency_overrides[get_db] = get_db


# Test for validation error when updating a todo
def test_update_todo_validation_error01(test_client):
    """
    Test case for validation error when updating a todo with incomplete data.
    Expects the response status code to be 422.
    """
    todo_data1 = {"todo": {"description": "Test Description"}}
    response1 = test_client.put("/api/todos/{1000}", json=todo_data1)
    assert response1.status_code == 422


# Test for updating a non-existent todo
def test_update_todo_empty(test_client):
    """
    Test case for updating a non-existent todo.
    Expects the response status code to be 404 and a detail message indicating
    that the todo is not found.
    """
    todo_data1 = {"todo": {"title": "Test01", "description": "Test Description"}}
    id = 25000
    response = test_client.put(f"/api/todos/{id}", json=todo_data1)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


@pytest.mark.xfail
def test_update_todo_internal_server_error(test_client):
    """
    Test case for updating a todo with a simulated internal server error.

    This test uses a mocked dependency to simulate an internal server error during database access.

    Args:
        test_client: Test client for the FastAPI application.

    Raises:
        AssertionError: If the response status code is not 500.

    """

    def mock_get_db():
        raise Exception("Mocked exception in get_db")

    app.dependency_overrides[get_db] = mock_get_db
    try:
        todo_data1 = {"todo": {"title": "Test01", "description": "Test Description"}}
        response = test_client.put("/api/todos/{1}", json=todo_data1)
        assert response.status_code == 500
    finally:
        app.dependency_overrides[get_db] = get_db


def test_create_todo_success(test_client):
    """
    Test case for creating a todo successfully and then updating it.

    This test creates a todo, updates it, and then verifies that the update was successful.

    Args:
        test_client: Test client for the FastAPI application.

    Raises:
        AssertionError: If any of the assertions fail.

    """
    todo_data = {"todo": {"title": "Test Todo 1", "description": "Test Description 1"}}
    response = test_client.post("/api/todos", json=todo_data)
    added_todo = response.json()
    id = added_todo["id"]
    updated_data = {
        "todo": {
            "title": "Test Todo updated",
            "description": "Test Description updated",
        }
    }
    response = test_client.put(f"/api/todos/{id}", json=updated_data)
    updated_todo = response.json()
    id1 = updated_todo["id"]
    test_client.delete(f"/api/todos/{id1}")

    # Assertions to verify the success of the update
    assert response.status_code == 200
    assert id1 == added_todo["id"]
    assert updated_todo["title"] == updated_data["todo"]["title"]
    assert updated_todo["description"] == updated_data["todo"]["description"]
