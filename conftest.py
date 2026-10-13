from decimal import Decimal

import pytest

from apps.donation.choices import DonationMethod
from apps.donation.models import Donation
from apps.group.models import Regional, TertiaryGroup
from apps.user.choices import UserLevel
from apps.user.models import User


@pytest.fixture
def regional():
    return Regional.objects.create(name='South')


@pytest.fixture
def tertiarygroup(regional):
    return TertiaryGroup.objects.create(name='Central Church', regional=regional)


@pytest.fixture
def sibling_tertiarygroup(regional):
    return TertiaryGroup.objects.create(name='North Church', regional=regional)


@pytest.fixture
def foreign_tertiarygroup():
    return TertiaryGroup.objects.create(
        name='Far Church', regional=Regional.objects.create(name='East')
    )


@pytest.fixture
def tertiarygroup_user(tertiarygroup):
    return User.objects.create_user(
        username='church-user', level=UserLevel.TERTIARYGROUP, tertiarygroup=tertiarygroup
    )


@pytest.fixture
def regional_user(regional):
    return User.objects.create_user(
        username='regional-user', level=UserLevel.REGIONAL, regional=regional
    )


@pytest.fixture
def donation_factory():
    def create(tertiarygroup, **kwargs):
        defaults = {
            'donor_name': 'Maria',
            'amount': Decimal('50.00'),
            'method': DonationMethod.PIX,
        }
        return Donation.objects.create(tertiarygroup=tertiarygroup, **{**defaults, **kwargs})

    return create
