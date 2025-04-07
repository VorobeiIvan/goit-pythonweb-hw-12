import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Base URL for generating links in emails
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def send_email(to_email, subject, body):
    """
    Send a generic email using the SMTP protocol.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body content of the email.

    Logs:
        Logs success or failure of the email sending process.
    """
    # Create a plain text email message
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"  # Sender's email address
    msg["To"] = to_email  # Recipient's email address

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        # Log any errors that occur during the email sending process
        logger.error(f"Failed to send email to {to_email}: {e}")


def send_verification_email(email: str, token: str):
    """
    Send a verification email to the user with a unique verification link.

    Args:
        email (str): The recipient's email address.
        token (str): The unique verification token.

    The email contains a link that the user can click to verify their email address.
    """
    # Generate the verification URL
    verification_url = f"{BASE_URL}/verify/{token}"
    # Email body content
    body = f"Please verify your email by clicking the link: {verification_url}"
    # Send the email
    send_email(email, "Verify your email", body)


def send_password_reset_email(email: str, token: str):
    """
    Send a password reset email to the user with a unique reset link.

    Args:
        email (str): The recipient's email address.
        token (str): The unique password reset token.

    The email contains a link that the user can click to reset their password.
    """
    # Generate the password reset URL
    reset_url = f"{BASE_URL}/reset-password/{token}"
    # Email body content
    body = f"Click the link to reset your password: {reset_url}"
    # Send the email
    send_email(email, "Reset your password", body)
