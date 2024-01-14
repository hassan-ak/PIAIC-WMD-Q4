"""
Module: test_database.py

This script contains tests for the database connection functionality.

It covers the following aspects:
- Loading environment variables
- Checking the existence of the 'DB_URL' environment variable
- Creating an SQLAlchemy engine
- Creating a local session using SQLAlchemy sessionmaker
- Establishing a connection to the database using the engine
- Executing a query using the local session

These tests help ensure the proper setup and functionality of the database-related code.
"""

# Import necessary libraries
import os
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

# Importing functions and objects from the app
from database_connection.database import (
    load_environment_variables,
    create_local_session,
    local_session,
)


def test_load_environment_variables():
    """
    Test whether environment variables are loaded successfully.
    """
    assert load_environment_variables() is True


def test_database_url_exists():
    """
    Test whether the 'DB_URL' environment variable is set.
    """
    assert os.environ.get("DB_URL") is not None


def test_create_sqlalchemy_engine():
    """
    Test whether the SQLAlchemy engine is created successfully.
    """
    engine = create_engine(os.environ.get("DB_URL"))
    assert isinstance(engine, Engine)


def test_create_local_session():
    """
    Test whether the local session is created successfully.
    """
    session_maker = create_local_session()
    assert isinstance(session_maker, sessionmaker)
    session = session_maker()
    assert isinstance(session, Session)


def test_engine_connection():
    """
    Test whether the engine can establish a connection to the database.
    """
    engine = create_engine(os.environ.get("DB_URL"))
    connection = None
    try:
        connection = engine.connect()
        assert connection is not None
    finally:
        if connection:
            connection.close()


def test_session_query():
    """
    Test whether a query can be executed using the local session.
    """
    db = local_session()
    try:
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        db.close()
