import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
import os
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def send_email(to_email, subject, body):
    """
    Send a generic email.

    Args:
        to_email (str): The recipient's email address.
        subject (str): The email subject.
        body (str): The email body.
    """
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "noreply@example.com"
    msg["To"] = to_email

    try:
        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)
        logger.info(f"Email sent to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


def send_verification_email(email: str, token: str):
    """
    Send a verification email to the user.

    Args:
        email (str): The recipient's email address.
        token (str): The verification token.
    """
    verification_url = f"{BASE_URL}/verify/{token}"
    body = f"Please verify your email by clicking the link: {verification_url}"
    send_email(email, "Verify your email", body)


def send_password_reset_email(email: str, token: str):
    """
    Send a password reset email to the user.

    Args:
        email (str): The recipient's email address.
        token (str): The password reset token.
    """
    reset_url = f"{BASE_URL}/reset-password/{token}"
    body = f"Click the link to reset your password: {reset_url}"
    send_email(email, "Reset your password", body)
