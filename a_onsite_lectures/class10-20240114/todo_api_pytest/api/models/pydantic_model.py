"""
Module: pydantic_model.py

This module contains Pydantic models for representing TODO items.

- TodoBaseModel: Base Pydantic model for the basic structure of a TODO item.
- TodoResponseModel: Pydantic model for the response structure of a TODO item.
"""
from pydantic import BaseModel


# Define a base Pydantic model for representing the basic structure of a TODO item.
class TodoBaseModel(BaseModel):
    """
    Base Pydantic model representing the basic structure of a TODO item.

    Attributes:
        title (str): The title of the TODO item.
        description (str): The description of the TODO item.
    """

    # The title of the TODO item, expected to be a string.
    title: str
    # The description of the TODO item, expected to be a string.
    description: str


# Define a Pydantic model for representing the response structure of a TODO item.
# Extends TodoBaseModel to inherit the properties defined in TodoBaseModel.
class TodoResponseModel(TodoBaseModel):
    """
    Pydantic model representing the response structure of a TODO item.

    Inherits from TodoBaseModel to reuse properties defined in TodoBaseModel.

    Attributes:
        id (int): The unique identifier (ID) of the TODO item.
    """

    # The unique identifier (ID) of the TODO item, expected to be an integer.
    id: int
