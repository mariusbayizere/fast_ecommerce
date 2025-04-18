from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Integer, String
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
from enum import Enum

class UserRole(str, Enum):
    """This class is responsible for defining the user role
    and its possible values.
    The UserRole class inherits from the str and Enum classes.
    This allows us to define a set of named values that represent
    different user roles in the system.

    Args:
        str (_type_): This class is responsible for defining the user role
        Enum (_type_): This class is responsible for defining the user role
    """
    admin = "admin"
    User = "User"


class User(SQLModel, table=True):
    """This class is responsible for defining the user model
    and its possible values.

    Args:
        SQLModel (_type_): This class is responsible for defining the user model
        table (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """

    __tablename__ = "users"
    id: int = Field(sa_column=Column(Integer, primary_key=True, nullable=False, autoincrement=True))
    username: str = Field(sa_column=Column(String, nullable=False, unique=True))
    email: str = Field(sa_column=Column(String, nullable=False, unique=True))
    password: str = Field(sa_column=Column(String, nullable=False))
    role: UserRole = Field(default=UserRole.User, sa_column=Column(String, nullable=False)) 
    is_active: bool = Field(default=True, nullable=False)
    created_date : datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.utcnow, nullable=False))




    def __repr__(self):
        """This function is responsible for returning the user information
        in a readable format.

        Returns:
            _type_: return user information
        """
        return (
            f"User(id={self.id}, "
            f"username='{self.username}', "
            f"email='{self.email}', "
            f"password='{self.password}', "
            f"role='{self.role}', "
            f"is_active='{self.is_active}', "
            f"created_date='{self.created_date}')"
        )
    

    def __str__(self):
        """This function is responsible for returning the user information
        in a readable format.

        Returns:
            _type_: return user information
        """
        return (
            f"User(id={self.id}, "
            f"username='{self.username}', "
            f"email='{self.email}', "
            f"password='{self.password}', "
            f"role='{self.role}', "
            f"is_active='{self.is_active}', "
            f"created_date='{self.created_date}')"
        )