from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Form, Request, Response
from datetime import timedelta
import uuid
import bcrypt
from fastapi.responses import RedirectResponse

from src.database.model import User
from src.database.db import find_one_user, write_new_user, update_one_user_token
from src.services.auth import create_access_token, get_current_user
from src.conf.config import config
from src.services.email import send_confirmation_email

router = APIRouter()

@router.get("/register")
async def register_page(request: Request):
    """
    Renders the registration page.

    Args:
    - request (Request): The request object containing metadata about the request.

    Returns:
    - TemplateResponse: The rendered HTML page for registration.
    """
    return config.TEMPLATES.TemplateResponse("registration.html", {"request": request})

@router.post("/register")
async def register(
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    """
    Handles user registration, including validation, password hashing, and email confirmation.

    Args:
    - request (Request): The request object containing metadata about the request.
    - response (Response): The response object used to manage the HTTP response.
    - background_tasks (BackgroundTasks): Background tasks for handling email sending.
    - username (str): The username of the user registering.
    - email (str): The email of the user registering.
    - password (str): The password of the user registering.

    Returns:
    - RedirectResponse: Redirects to the home page upon successful registration.

    Raises:
    - HTTPException: If the email is already registered, an HTTP 400 error is raised.
    """
    existing_user = await find_one_user({"email": email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    confirmation_token = str(uuid.uuid4())

    new_user = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "is_active": False,
        "confirmation_token": confirmation_token
    }
    await write_new_user(new_user)
    background_tasks.add_task(send_confirmation_email, email, confirmation_token, config.BASE_URL)

    return RedirectResponse(url="/", status_code=302)

@router.get("/confirm/{token}")
async def confirm_email(token: str):
    """
    Confirms a user's email address using the provided confirmation token.

    Args:
    - token (str): The confirmation token sent to the user's email.

    Returns:
    - dict: A message indicating the success of the email confirmation.

    Raises:
    - HTTPException: If the token is invalid or not found, an HTTP 400 error is raised.
    """
    user = await find_one_user({"confirmation_token": token})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    await update_one_user_token({"confirmation_token": token}, {"$set": {"is_active": True, "confirmation_token": None}})
    return RedirectResponse(url="/", status_code=302)

@router.get("/login")
async def login_page(request: Request):
    """
    Renders the login page.

    Args:
    - request (Request): The request object containing metadata about the request.

    Returns:
    - TemplateResponse: The rendered HTML page for login.
    """
    return config.TEMPLATES.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    response: Response,
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    """
    Handles user login, including authentication and setting the access token cookie.

    Args:
    - response (Response): The response object used to manage the HTTP response.
    - username (str): The username of the user attempting to log in.
    - password (str): The password of the user attempting to log in.

    Returns:
    - RedirectResponse: Redirects to the home page upon successful login.

    Raises:
    - HTTPException: If the username or password is invalid, or if the email is not confirmed, an HTTP 401 or 400 error is raised.
    """
    db_user = await find_one_user({"username": username})
    if not db_user:
        return config.TEMPLATES.TemplateResponse(
        "invalid_username_password.html",
        {"request": request}
        )

    if not bcrypt.checkpw(password.encode('utf-8'), db_user["hashed_password"].encode('utf-8')):
        return config.TEMPLATES.TemplateResponse(
        "invalid_username_password.html",
        {"request": request}
        )

    if not db_user["is_active"]:
        raise HTTPException(status_code=400, detail="Email not confirmed")

    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["username"]}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/", status_code=302)
    response.set_cookie(key="access_token", value=access_token, httponly=True, path="/")

    return response

@router.get("/logout")
async def logout(response: Response):
    """
    Logs the user out by clearing the access token cookie.

    Args:
    - response (Response): The response object used to manage the HTTP response.

    Returns:
    - RedirectResponse: Redirects to the login page after logging out.
    """
    response.set_cookie(key="access_token", value="", expires=0, httponly=True, path="/")
    return RedirectResponse(url="/auth/login", status_code=302)

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Retrieves the currently authenticated user's information.

    Args:
    - current_user (User): The currently authenticated user obtained from dependency injection.

    Returns:
    - dict: A dictionary containing the current user's username and email.
    """
    return {"username": current_user.username, "email": current_user.email}