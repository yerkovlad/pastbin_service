from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Request

from src.conf.config import config
from src.database.db import find_one_user
from src.database.model import User

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates an access token for authentication.

    Args:
    - data (dict): The payload data to include in the token.
    - expires_delta (timedelta, optional): The duration after which the token will expire. If not provided, defaults to 15 minutes.

    Returns:
    - str: The encoded JWT access token.

    Notes:
    - If `expires_delta` is not provided, the token will expire in 15 minutes from the time of creation.
    - The token is encoded using the secret key and algorithm specified in the configuration.
    """
    to_encode = data.copy()  # Create a copy of the data to avoid modifying the original
    if expires_delta:
        expire = datetime.utcnow() + expires_delta  # Set expiration time based on provided delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # Default expiration time of 15 minutes

    to_encode.update({"exp": expire})  # Add expiration time to the payload
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)  # Encode the JWT
    return encoded_jwt

async def get_current_user(request: Request) -> User:
    """
    Retrieves the currently authenticated user based on the access token in the request cookies.

    Args:
    - request (Request): The FastAPI request object containing the cookies.

    Returns:
    - User: An instance of the `User` model representing the currently authenticated user, or `None` if the user is not authenticated.

    Notes:
    - The function attempts to extract the `access_token` from cookies, decode it, and validate the user's existence in the database.
    - If the token is prefixed with "Bearer ", it is stripped before decoding.
    - If the token is invalid or the user does not exist, `None` is returned.
    """
    try:
        # Extract token from cookies
        token = request.cookies.get("access_token")
        if token is None:
            return None
        
        # Remove "Bearer " prefix if it exists
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]
        
        # Decode the token and extract the payload
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        
        # Check if user exists in the database
        user = await find_one_user({"username": username})
        if user is None:
            return None
        
        return User(username=user["username"], email=user["email"])
    except JWTError as e:
        # Log the error for debugging purposes
        print(f"JWT error: {e}")
        return None