"""
Module: sqlalchemy_model.py


This module defines SQLAlchemy models for a 'todos' table in a database.

Classes:
- Base: Base class for declarative models using SQLAlchemy ORM.
- Todo: Represents a 'todos' table with id, title, and description columns.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    """
    Base class for declarative models using SQLAlchemy ORM.
    """

    pass


class Todo(Base):
    """
    Represents a 'todos' table in a database using SQLAlchemy ORM.

    Attributes:
    - id: Primary key column for the Todo table (integer).
    - title: Title column for the Todo table (string, max length: 30 characters, non-nullable).
    - description: Description column for the Todo table (string, non-nullable).
    """

    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the Todo instance.

        Returns:
        - str: A string representation of the Todo instance, including id, title, and description.
        """
        return f"<Todo id={self.id}, title='{self.title}', description='{self.description}'>"
