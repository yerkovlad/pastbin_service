from fastapi import APIRouter, HTTPException, Depends, Request, Form

from src.services.auth import get_current_user
from src.repository.pastbin import past, read_message_with_id, all_text
from src.conf.config import config

router = APIRouter()

@router.get("/create_message")
async def create_message_page(request: Request):
    """
    Renders the page for creating a new message.

    Args:
    - request (Request): The request object containing metadata about the request.

    Returns:
    - TemplateResponse: The rendered HTML page for creating a message.
    """
    return config.TEMPLATES.TemplateResponse("create_message.html", {"request": request})

@router.post("/create_message")
async def create_message(
    request: Request,
    text: str = Form(...),
    current_user: dict = Depends(get_current_user),
):
    """
    Handles the creation of a new message by storing it and returning a page with the message's URL.

    Args:
    - request (Request): The request object containing metadata about the request.
    - text (str): The text content of the message being created.
    - current_user (dict): The currently authenticated user, obtained from the `get_current_user` dependency.

    Returns:
    - TemplateResponse: The rendered HTML page for message creation confirmation with the message URL.

    Notes:
    - The `username` is extracted from the `current_user` object.
    - The `message_id` is obtained from the `past` function, which stores the message and returns the ID.
    """
    username = current_user.username
    message_id = await past(username, text)
    return config.TEMPLATES.TemplateResponse(
        "message_created.html",
        {"request": request, "url": f"{config.BASE_URL}/pastbin/message/{message_id}"}
    )

@router.get("/message/{message_id}")
async def message(message_id: str, request: Request):
    """
    Retrieves and renders a message based on its ID.

    Args:
    - message_id (str): The ID of the message to be retrieved.
    - request (Request): The request object containing metadata about the request.

    Returns:
    - TemplateResponse: The rendered HTML page displaying the message details.

    Raises:
    - HTTPException: If the message is not found, an HTTP 404 error is raised.
    """
    output = await read_message_with_id(message_id)
    if output:
        return config.TEMPLATES.TemplateResponse(
            "message.html",
            {"request": request, "username": output["username"], "text": output["text"]}
        )
    raise HTTPException(status_code=404, detail="Message not found")

@router.get("/all_messages")
async def all_messages(request: Request):
    """
    Retrieves and renders a list of all messages.

    Args:
    - request (Request): The request object containing metadata about the request.

    Returns:
    - TemplateResponse: The rendered HTML page displaying all messages.
    """
    messages = await all_text()
    return config.TEMPLATES.TemplateResponse(
        "messages.html",
        {"request": request, "messages": messages}
    )