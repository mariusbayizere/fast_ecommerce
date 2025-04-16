from sqlmodel import Field, SQLModel, Relationship, Column
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy import Integer, String



 
class Student(SQLModel, table=True):
    __tablename__ = "students"
    id: int = Field(sa_column=Column(Integer,primary_key=True,nullable=False, autoincrement=True)) 
    FirstName: str = Field(sa_column=Column(String, nullable=False))
    LastName: str = Field(sa_column=Column(String,nullable=False))
    Email: str = Field(sa_column=Column(String,nullable=False, unique=True))
    PhoneNumber: str = Field(sa_column=Column(String, nullable=False, unique=True))
    Gender: str = Field(sa_column=Column(String,nullable=False))
    Nationality: str = Field(sa_column=Column(String, nullable=False))


    def __repr__(self):
        return (
            f"Student(id={self.id}, "
            f"first_name='{self.FirstName}', "
            f"last_name='{self.LastName}', "
            f"email='{self.Email}', "
            f"phone_number='{self.PhoneNumber}', "
            f"gender='{self.Gender}', "
            f"nationality='{self.Nationality}')"
        )