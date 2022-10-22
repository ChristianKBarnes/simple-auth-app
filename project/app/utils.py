from datetime import datetime, timedelta

from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import FastMail, MessageSchema
from passlib.context import CryptContext
from jose import jwt

from app.config.app import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.app_secret, algorithm=settings.app_hash_algorithm
    )
    return encoded_jwt


def send_email(
    background_tasks: BackgroundTasks,
    subject: str,
    email_to: str,
    body: dict,
    template_name: str,
):

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )

    fm = FastMail(settings.email_configuration)
    background_tasks.add_task(fm.send_message, message, template_name="test_email.html")
