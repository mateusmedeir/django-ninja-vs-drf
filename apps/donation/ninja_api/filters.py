from ninja import FilterSchema

from apps.donation.choices import DonationMethod, DonationStatus


class DonationFilterSchema(FilterSchema):
    status: DonationStatus | None = None
    method: DonationMethod | None = None
    tertiarygroup_id: int | None = None
