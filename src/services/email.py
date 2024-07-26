from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.conf.config import config

# Define the email configuration
conf = ConnectionConfig(
    MAIL_USERNAME="tryfastapi@meta.ua",
    MAIL_PASSWORD="Metasveta2024",
    MAIL_FROM="tryfastapi@meta.ua",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.meta.ua",
    MAIL_FROM_NAME="Pastbin",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)

async def send_confirmation_email(email: EmailStr, token: str, host: str):
    """
    Sends a confirmation email for email verification.

    This function sends an email to the user with a verification link that includes a token.
    The email template used for sending is specified as "verify_email.html".

    Args:
        email (EmailStr): The recipient's email address to which the verification email will be sent.
        token (str): The verification token to be included in the email. This token will be used to confirm the user's email.
        host (str): The base URL of the host where the verification link should point to.

    Raises:
        ConnectionErrors: If there is an issue connecting to the email server, such as authentication failure or network issues.
        Exception: For any other unexpected errors that may occur during the process.

    Notes:
        - The email configuration is set up to use SMTP with SSL/TLS.
        - Ensure that the email server credentials and configuration are correctly set.
        - The template for the email is located in the 'templates' folder relative to this file.
    """
    try:
        # Create a message schema with the necessary details
        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],  # List of recipient emails
            template_body={"token": token, "host": host},  # Data to be passed to the email template
            subtype=MessageType.html  # Email content type
        )
        # Initialize FastMail with the configured settings
        fm = FastMail(conf)
        # Send the email using the specified template
        await fm.send_message(message, template_name="verify_email.html")
    except ConnectionErrors as err:
        # Handle connection errors such as issues with the email server
        print(f"Connection error: {err}")
    except Exception as e:
        # Handle any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")