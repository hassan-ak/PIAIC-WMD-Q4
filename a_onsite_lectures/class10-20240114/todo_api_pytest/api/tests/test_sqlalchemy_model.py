"""
Module: test_sqlalchemy_model.py

This module contains unit tests for the SQLAlchemy models in the 'app.models.sqlalchemy_model' module.

Tested Classes and Functions:
- test_base_model: Test the instantiation of the Base class.
- test_repr_method: Test the __repr__ method of the Todo class.
- test_todo_attributes: Test the attributes of the Todo class.
"""

from models.sqlalchemy_model import Todo, Base
from sqlalchemy.orm import DeclarativeBase


def test_base_model():
    """
    Test the instantiation of the Base class.

    This function creates an instance of the `Base` class and asserts that it is an instance
    of `DeclarativeBase` from SQLAlchemy.

    Returns:
        None
    """

    baseModel = Base()
    assert isinstance(baseModel, DeclarativeBase)


def test_todo_attributes():
    """
    Test the attributes of the Todo class.

    This function creates an instance of the `Todo` class with specified attributes and asserts
    that its attributes have the expected values.

    Returns:
        None
    """

    todo = Todo(id=1, title="Test Todo", description="This is a test todo.")
    assert todo.id == 1
    assert todo.title == "Test Todo"
    assert todo.description == "This is a test todo."


def test_repr_method():
    """
    Test the __repr__ method of the Todo class.

    This function creates an instance of the `Todo` class with specified attributes and compares
    its representation with the expected string.

    Returns:
        None
    """

    todo = Todo(id=1, title="Test Todo", description="This is a test todo.")
    expected_repr = "<Todo id=1, title='Test Todo', description='This is a test todo.'>"
    assert repr(todo) == expected_repr
