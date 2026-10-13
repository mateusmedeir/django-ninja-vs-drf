from decimal import Decimal

from ninja import Field, Schema

from apps.donation.choices import DonationMethod, DonationStatus
from misc.ninja.schemas import TimestampedModelSchema


class TertiaryGroupOut(Schema):
    id: int
    name: str


class DonationIn(Schema):
    tertiarygroup_id: int
    donor_name: str = Field(min_length=1, max_length=120)
    amount: Decimal = Field(ge=Decimal('0.01'), max_digits=12, decimal_places=2)
    method: DonationMethod


class DonationOut(TimestampedModelSchema):
    id: int
    tertiarygroup: TertiaryGroupOut
    donor_name: str
    amount: Decimal
    method: DonationMethod
    status: DonationStatus
