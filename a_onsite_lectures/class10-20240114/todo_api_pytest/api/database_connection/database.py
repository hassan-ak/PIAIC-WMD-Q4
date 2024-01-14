"""
Module: database.py


This script demonstrates loading environment variables from a .env file,
retrieving a database URL from the environment, and creating a SQLAlchemy
engine and sessionmaker for interacting with a database.

It uses the `dotenv` library for loading environment variables and `sqlalchemy`
for managing database connections.
"""

# Import necessary libraries
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


def load_environment_variables():
    """
    Load environment variables from a .env file (if present).

    Returns:
        bool: True if environment variables were successfully loaded, False otherwise.
    """
    return load_dotenv(find_dotenv())


# Load environment variables from a .env file (if present)
environment_loaded: bool = load_environment_variables()

# Retrieve the database URL from the environment variables
DATABASE_URL = os.environ.get("DB_URL")

# Create a SQLAlchemy engine using the specified database URL
engine = create_engine(DATABASE_URL)


def create_local_session():
    """
    Create a sessionmaker that will be used to create sessions with the database.

    Returns:
        sqlalchemy.orm.session.Session: A sessionmaker object.
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a sessionmaker that will be used to create sessions with the database
local_session = create_local_session()
