from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    userID: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    mobile_number: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)


class Student(User):
    __tablename__ = "students"
    studentID = Column(String, primary_key=True)


# class Instructor(User):
#     __tablename__ = "instructors"
#     instructorID = Column(String, primary_key=True)
