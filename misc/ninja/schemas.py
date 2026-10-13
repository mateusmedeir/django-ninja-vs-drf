from datetime import datetime

from ninja import Schema


class TimestampedModelSchema(Schema):
    created_at: datetime
    updated_at: datetime


class ErrorResponse(Schema):
    detail: str
