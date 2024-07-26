from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    UserCreate represents the data required for creating a new user.

    Attributes:
    - username (str): The username of the user.
    - email (EmailStr): The email address of the user, validated as a proper email format.
    - password (str): The password chosen by the user.
    """
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    UserLogin represents the data required for a user to log in.

    Attributes:
    - username (str): The username of the user.
    - password (str): The password of the user.
    """
    username: str
    password: str

class User(BaseModel):
    """
    User represents a user's publicly accessible information.

    Attributes:
    - username (str): The username of the user.
    - email (str): The email address of the user.
    """
    username: str
    email: str