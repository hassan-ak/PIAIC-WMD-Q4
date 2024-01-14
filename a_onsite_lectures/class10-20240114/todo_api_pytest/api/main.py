import json
"""
Module: main.py

This module implements a simple FastAPI application with CRUD (Create, Read, Update, Delete)
operations for managing Todo items. It utilizes Pydantic for data validation and SQLAlchemy
for interacting with the database.

Endpoints:
- POST /api/todos: Create a new Todo.
- GET /api/todos: Get all Todos.
- GET /api/todos/{todo_id}: Get a specific Todo by ID.
- DELETE /api/todos/{todo_id}: Delete a Todo by ID.
- PUT /api/todos/{todo_id}: Update a Todo by ID.

Dependencies:
- FastAPI: A modern, fast (high-performance), web framework for building APIs.
- Pydantic: Data validation and parsing using Python type hints.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) for Python.

Usage:
- Run the application using Uvicorn:
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
"""

# Import necessary modules and classes from FastAPI, Pydantic, and SQLAlchemy
from fastapi import FastAPI, Body, Depends, HTTPException, status
from pydantic import ValidationError
from database_connection.database import local_session
from models.pydantic_model import TodoBaseModel, TodoResponseModel
from sqlalchemy.orm import Session
from models.sqlalchemy_model import Todo

# Create a FastAPI instance
app = FastAPI()

# Dependency function to get the database session
def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()

# Define an endpoint to create a new Todo
@app.post("/api/todos")
def create_todo(
    todo: TodoBaseModel = Body(embed=True), db: Session = Depends(get_db)
) -> TodoResponseModel:
    """
    Create a new Todo.

    Parameters:
        - todo: TodoBaseModel, Pydantic model for request input.
        - db: SQLAlchemy Session, database session dependency.

    Returns:
        TodoResponseModel: Pydantic model for response.
    """
    try:
        # Create a new Todo in the database
        db_todo = Todo(title=todo.title, description=todo.description)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except ValidationError as e:
        # Handle validation errors
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e.errors()))
    except Exception as e:
        # Handle other exceptions
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Define an endpoint to get all Todos
@app.get("/api/todos")
def get_todos(db: Session = Depends(get_db)) -> list[TodoResponseModel]:
    """
    Get all Todos.

    Parameters:
        - db: SQLAlchemy Session, database session dependency.

    Returns:
        List[TodoResponseModel]: List of Pydantic models for response.
    """
    try:
        # Retrieve all Todos from the database
        todos = db.query(Todo).all()
        return todos
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Define an endpoint to get a specific Todo by ID
@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> TodoResponseModel:
    """
    Get a specific Todo by ID.

    Parameters:
        - todo_id: int, Todo ID.
        - db: SQLAlchemy Session, database session dependency.

    Returns:
        TodoResponseModel: Pydantic model for response.
    """
    try:
        # Query the database for the Todo with the specified ID
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except HTTPException:
        # Handle HTTP exceptions
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))

# Define an endpoint to delete a Todo by ID
@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Delete a Todo by ID.

    Parameters:
        - todo_id: int, Todo ID.
        - db: SQLAlchemy Session, database session dependency.

    Returns:
        dict: A dictionary with a success message.
    """
    try:
        # Delete the Todo from the database
        db.query(Todo).filter(Todo.id == todo_id).delete()
        db.commit()
        return {"message": "Todo deleted successfully"}
    except Exception as e:
        # Handle exceptions
        raise HTTPException(status_code=500, detail=str(e))

# Define an endpoint to update a Todo by ID
@app.put("/api/todos/{todo_id}")
def update_todo(
    todo_id: int, todo: TodoBaseModel = Body(embed=True), db: Session = Depends(get_db)
) -> TodoResponseModel:
    """
    Update a Todo by ID.

    Parameters:
        - todo_id: int, Todo ID.
        - todo: TodoBaseModel, Pydantic model for request input.
        - db: SQLAlchemy Session, database session dependency.

    Returns:
        TodoResponseModel: Pydantic model for response.
    """
    try:
        # Query the database for the Todo with the specified ID
        db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if db_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")

        # Update Todo fields
        db_todo.title = todo.title
        db_todo.description = todo.description

        db.commit()
        db.refresh(db_todo)
        return db_todo
    except ValidationError as e:
        # Handle validation errors
        db.rollback()
        raise HTTPException(status_code=422, detail=str(e.errors()))
    except HTTPException:
        # Handle HTTP exceptions
        raise HTTPException(status_code=404, detail="Todo not found")
    except Exception as e:
        # Handle other exceptions
        raise HTTPException(status_code=500, detail=str(e))

# Run the FastAPI app using Uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
