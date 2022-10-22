from datetime import date
from pydantic import BaseModel, EmailStr


class GuardianBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    other_names: str | None
    email: EmailStr | None
    identification_document_type: str | None
    identification_document_number: str | None
    identification_document_expiry: date | None


class GuardianCreate(GuardianBase):
    pass


class GuardianResponse(GuardianBase):
    id: int


class GuardianUpdate(GuardianBase):
    first_name: str | None
    last_name: str | None
    phone: str | None
