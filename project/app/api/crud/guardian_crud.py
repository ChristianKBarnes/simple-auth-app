import datetime
from typing import List

from tortoise.expressions import Q

from app.schemas.guardian import GuardianBase, GuardianCreate
from app.models.guardian import Guardian


async def post(payload: GuardianCreate) -> dict | None:
    guardian = Guardian(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
    )
    await guardian.save()

    return guardian


async def get(id: int | List) -> dict | List | None:
    if type(id) == list:
        guardian = await Guardian.filter(id__in=id).values()
    else:
        guardian = await Guardian.filter(Q(id=id) & Q(deleted_at=None)).first()

    if guardian:
        return guardian
    return None


async def get_guardian_by_phone(phone: str) -> dict | None:
    guardian = await Guardian.filter(
        Q(phone__endswith=phone[-9:]) & Q(deleted_at=None)
    ).first()
    if guardian:
        return guardian
    return None


async def get_all() -> List:
    guardians = await Guardian.filter(deleted_at=None).values()
    return guardians


async def delete(id: int) -> int | None:
    guardian = await Guardian.filter(Q(id=id) & Q(deleted_at=None)).update(
        deleted_at=datetime.datetime.now()
    )
    if guardian:
        return guardian
    return None


async def put(id: int, payload: GuardianBase) -> dict | None:
    guardian = await Guardian.filter(Q(id=id) & Q(deleted_at=None)).update(
        **payload.dict(exclude_unset=True)
    )
    if guardian:
        updated_guardian = await Guardian.filter(id=id).first()
        return updated_guardian
    return None
