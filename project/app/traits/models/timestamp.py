from tortoise import fields


class Timestamp:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now_add=True)
    deleted_at = fields.DatetimeField(null=True)
