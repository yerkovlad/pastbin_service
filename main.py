from fastapi import FastAPI, Request, Depends
import asyncio
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from src.repository.free_urls import free_urls
from src.routes import auth, pastbin
from src.conf.config import config
from src.services.auth import get_current_user
from src.database.model import User

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(pastbin.router, prefix="/pastbin", tags=["pastbin"])

@app.get("/")
async def index(request: Request, current_user: User = Depends(get_current_user)):
    """
    Handles requests to the root URL ("/").

    Parameters:
    - request: The HTTP request object.
    - current_user: The currently authenticated user, fetched using dependency injection.

    Actions:
    - Checks if the user is logged in by inspecting `current_user`.
    - If not logged in, redirects the user to the login page.
    - If logged in, performs an asynchronous operation to fetch or process URLs.
    - Finally, renders the `index.html` template, passing the user's information.

    Returns:
    - A RedirectResponse to the login page if the user is not authenticated.
    - A TemplateResponse with the rendered HTML page and user information if the user is authenticated.
    """
    
    # Check if there is a logged-in user. If not, redirect to the login page.
    if current_user is None:
        return RedirectResponse(url="/auth/login")

    # Call the free_urls function to possibly fetch or process some URLs.
    await free_urls()

    # Render the index.html template with the user's information.
    return config.TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "username": current_user.username, "email": current_user.email}
    )