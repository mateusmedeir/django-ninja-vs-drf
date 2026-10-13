from django.db import models

from apps.donation.choices import DonationMethod, DonationStatus
from apps.donation.querysets import DonationQuerySet


class Donation(models.Model):
    tertiarygroup = models.ForeignKey(
        'group.TertiaryGroup', on_delete=models.PROTECT, related_name='donations'
    )
    donor_name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    method = models.CharField(max_length=20, choices=DonationMethod.choices)
    status = models.CharField(
        max_length=20, choices=DonationStatus.choices, default=DonationStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DonationQuerySet.as_manager()
