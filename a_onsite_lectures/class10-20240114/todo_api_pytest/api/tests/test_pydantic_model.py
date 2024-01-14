"""
Module: test_pydantic_model.py

This module contains tests for the TodoBaseModel and TodoResponseModel
defined in the app.models.pydantic_model module.
"""
from models.pydantic_model import TodoBaseModel, TodoResponseModel
import pytest
from pydantic import ValidationError


# Test cases for TodoBaseModel
def test_create_todo_base_model():
    """
    Test creating a TodoBaseModel with valid data.
    """
    data = {"title": "Task 1", "description": "Description for Task 1"}
    todo_base_model = TodoBaseModel(**data)
    assert todo_base_model.title == "Task 1"
    assert todo_base_model.description == "Description for Task 1"


def test_create_todo_base_model_missing_title():
    """
    Test raising ValueError when title is missing.
    """
    with pytest.raises(ValueError):
        data = {"description": "Description for Task 1"}
        TodoBaseModel(**data)


def test_create_todo_base_model_missing_description():
    """
    Test raising ValueError when description is missing.
    """
    with pytest.raises(ValueError):
        data = {"title": "Task 1"}
        TodoBaseModel(**data)


def test_create_todo_base_model_validate_title():
    """
    Test raising ValidationError for invalid title.
    """
    with pytest.raises(
        ValidationError, match="1 validation error for TodoBaseModel\ntitle"
    ):
        TodoBaseModel(description="Description for Task 2")


def test_create_todo_base_model_validate_description():
    """
    Test raising ValidationError for invalid description.
    """
    with pytest.raises(
        ValidationError, match="1 validation error for TodoBaseModel\ndescription"
    ):
        TodoBaseModel(title="Task 2")


# Test cases for TodoResponseModel
def test_create_todo_response_model():
    """
    Test creating a TodoResponseModel with valid data.
    """
    data = {"title": "Task 1", "description": "Description for Task 1", "id": 1}
    todo_response_model = TodoResponseModel(**data)
    assert todo_response_model.title == "Task 1"
    assert todo_response_model.description == "Description for Task 1"
    assert todo_response_model.id == 1


def test_create_todo_response_model_missing_id():
    """
    Test raising ValueError when id is missing.
    """
    with pytest.raises(ValueError):
        data = {"title": "Task 1", "description": "Description for Task 1"}
        TodoResponseModel(**data)


def test_create_todo_response_model_missing_title():
    """
    Test raising ValueError when title is missing.
    """
    with pytest.raises(ValueError):
        data = {"description": "Description for Task 1", "id": 1}
        TodoResponseModel(**data)


def test_create_todo_response_model_missing_description():
    """
    Test raising ValueError when description is missing.
    """
    with pytest.raises(ValueError):
        data = {"title": "Task 1", "id": 1}
        TodoResponseModel(**data)


def test_create_todo_response_model_validate_id():
    """
    Test raising ValidationError for invalid id.
    """
    with pytest.raises(
        ValidationError, match="1 validation error for TodoResponseModel\nid"
    ):
        TodoResponseModel(title="Task 2", description="Description for Task 2")


def test_create_todo_response_model_validate_title():
    """
    Test raising ValidationError for invalid title.
    """
    with pytest.raises(
        ValidationError, match="1 validation error for TodoResponseModel\ntitle"
    ):
        TodoResponseModel(description="Description for Task 2", id=2)


def test_create_todo_response_model_validate_description():
    """
    Test raising ValidationError for invalid description.
    """
    with pytest.raises(
        ValidationError, match="1 validation error for TodoResponseModel\ndescription"
    ):
        TodoResponseModel(title="Task 2", id=2)
