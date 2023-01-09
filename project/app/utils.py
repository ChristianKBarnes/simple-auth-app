import io
from datetime import datetime, timedelta

from fastapi import BackgroundTasks, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi_mail import FastMail, MessageSchema
from passlib.context import CryptContext
from jose import jwt
import qrcode

from app.config.app import Settings, get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    settings = get_settings()
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
    email_to: list,
    body: dict,
    template_name: str,
    settings: Settings = Depends(get_settings),
    attachments: list = [] 
) -> None:

    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        template_body=body,
        subtype="html",
        attachments=attachments,
    )

    fm = FastMail(settings.email_configuration)
    background_tasks.add_task(fm.send_message, message, template_name=template_name)


def send_multiple_emails(
    background_tasks: BackgroundTasks,
    subject: str,
    recipients: list,
    body: dict,
    template_name: str,
    settings: Settings = Depends(get_settings),
) -> None:
    for recipient in recipients:
        body["guardian_name"] = recipient["name"]
        send_email(
            background_tasks,
            subject=subject,
            email_to=[recipient["email"]],
            body=body,
            template_name=template_name,
            settings=settings,
        )


def generate_qrcode(data):
    code_image = qrcode.make(data)
    response_buffer = io.BytesIO()
    code_image.save(response_buffer)
    response_buffer.seek(0)

    return response_buffer
