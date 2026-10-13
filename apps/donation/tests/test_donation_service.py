from decimal import Decimal

import pytest

from apps.donation.choices import DonationMethod, DonationStatus
from apps.donation.exceptions import DonationNotCancelableError, TertiaryGroupOutOfScopeError
from apps.donation.services.donation_service import DonationService


@pytest.mark.django_db
class TestDonationService:
    def test_create_donation_starts_pending(self, tertiarygroup_user, tertiarygroup):
        donation = DonationService.create_donation(
            user=tertiarygroup_user,
            tertiarygroup_id=tertiarygroup.id,
            donor_name='Maria',
            amount=Decimal('50.00'),
            method=DonationMethod.PIX,
        )

        assert donation.status == DonationStatus.PENDING
        assert donation.tertiarygroup == tertiarygroup

    def test_create_donation_refuses_tertiarygroup_outside_user_scope(
        self, tertiarygroup_user, sibling_tertiarygroup
    ):
        with pytest.raises(TertiaryGroupOutOfScopeError):
            DonationService.create_donation(
                user=tertiarygroup_user,
                tertiarygroup_id=sibling_tertiarygroup.id,
                donor_name='Maria',
                amount=Decimal('50.00'),
                method=DonationMethod.PIX,
            )

    def test_cancel_donation_cancels_pending(self, tertiarygroup, donation_factory):
        donation = donation_factory(tertiarygroup)

        DonationService.cancel_donation(donation)

        donation.refresh_from_db()
        assert donation.status == DonationStatus.CANCELED

    def test_cancel_donation_refuses_paid(self, tertiarygroup, donation_factory):
        donation = donation_factory(tertiarygroup, status=DonationStatus.PAID)

        with pytest.raises(DonationNotCancelableError):
            DonationService.cancel_donation(donation)
