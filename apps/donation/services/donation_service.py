from decimal import Decimal

from apps.donation.choices import DonationStatus
from apps.donation.exceptions import DonationNotCancelableError, TertiaryGroupOutOfScopeError
from apps.donation.models import Donation
from apps.group.models import TertiaryGroup


class DonationService:
    @staticmethod
    def create_donation(
        *, user, tertiarygroup_id: int, donor_name: str, amount: Decimal, method: str
    ) -> Donation:
        """Registers a pending donation for a tertiarygroup within the user's scope."""
        tertiarygroup = TertiaryGroup.objects.visible_to(user).filter(id=tertiarygroup_id).first()
        if not tertiarygroup:
            raise TertiaryGroupOutOfScopeError()

        return Donation.objects.create(
            tertiarygroup=tertiarygroup, donor_name=donor_name, amount=amount, method=method
        )

    @staticmethod
    def cancel_donation(donation: Donation) -> Donation:
        if donation.status != DonationStatus.PENDING:
            raise DonationNotCancelableError()

        donation.status = DonationStatus.CANCELED
        donation.save(update_fields=['status', 'updated_at'])
        return donation
