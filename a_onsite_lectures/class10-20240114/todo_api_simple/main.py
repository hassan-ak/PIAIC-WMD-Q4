from fastapi import FastAPI, Body, Depends
from database import Todo, local_session
from model import TODOBase, TODOResponse
from sqlalchemy.orm import Session

app = FastAPI()


def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/todos")
def create_todo(
    todo: TODOBase = Body(embed=True), db: Session = Depends(get_db)
) -> TODOResponse:
    db_todo = Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/api/todos")
def get_todos(db: Session = Depends(get_db)) -> list[TODOResponse]:
    return db.query(Todo).all()


@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)) -> TODOResponse:
    return db.query(Todo).filter(Todo.id == todo_id).first()


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)) -> dict:
    db.query(Todo).filter(Todo.id == todo_id).delete()
    db.commit()
    return {"message": "Todo deleted successfully"}


@app.put("/api/todos/{todo_id}")
def update_todo(
    todo_id: int, todo: TODOBase = Body(embed=True), db: Session = Depends(get_db)
) -> TODOResponse:
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db_todo.title = todo.title
    db_todo.description = todo.description
    db.commit()
    db.refresh(db_todo)
    return db_todo
