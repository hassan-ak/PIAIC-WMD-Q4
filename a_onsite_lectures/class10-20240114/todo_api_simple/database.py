from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String
from sqlalchemy import create_engine

_: bool = load_dotenv(find_dotenv())

DATABASE_URL = os.environ.get("DB_URL")

engine = create_engine(DATABASE_URL)

local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass

class Todo(Base):
    __tablename__ = "todos"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Todo {self.title}>"
