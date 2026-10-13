from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.donation.choices import DonationMethod, DonationStatus
from apps.donation.models import Donation
from apps.group.models import Regional, TertiaryGroup
from apps.user.choices import UserLevel
from apps.user.models import AccessToken, User


class Command(BaseCommand):
    help = 'Creates demo regionals, tertiarygroups, users with tokens and donations.'

    @transaction.atomic
    def handle(self, *args, **options):
        south = Regional.objects.create(name='South')
        east = Regional.objects.create(name='East')
        central = TertiaryGroup.objects.create(name='Central Church', regional=south)
        north = TertiaryGroup.objects.create(name='North Church', regional=south)
        far = TertiaryGroup.objects.create(name='Far Church', regional=east)

        users = [
            User.objects.create_user(
                username='church-user', level=UserLevel.TERTIARYGROUP, tertiarygroup=central
            ),
            User.objects.create_user(
                username='regional-user', level=UserLevel.REGIONAL, regional=south
            ),
            User.objects.create_superuser(username='admin', password='admin'),
        ]

        methods = list(DonationMethod)
        statuses = list(DonationStatus)
        Donation.objects.bulk_create(
            Donation(
                tertiarygroup=tertiarygroup,
                donor_name=f'Donor {index}',
                amount=Decimal(10 + index),
                method=methods[index % len(methods)],
                status=statuses[index % len(statuses)],
            )
            for index, tertiarygroup in enumerate([central, north, far] * 10)
        )

        for user in users:
            token = AccessToken.objects.create(user=user)
            self.stdout.write(f'{user.username:<15} Bearer {token.key}')
