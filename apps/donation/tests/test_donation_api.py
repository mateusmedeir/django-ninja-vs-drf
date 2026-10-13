import pytest

from apps.donation.choices import DonationStatus
from misc.tests.mixin import AuthRequestMixin


class DonationApiContract(AuthRequestMixin):
    """The behaviour both edges must share. Each subclass points it at one framework."""

    items_key: str
    validation_status_code: int

    def test_list_requires_authentication(self, client):
        response = self.auth_get(client)

        assert response.status_code == 401

    def test_list_shows_only_donations_of_the_user_tertiarygroup(
        self, client, tertiarygroup_user, tertiarygroup, sibling_tertiarygroup, donation_factory
    ):
        own = donation_factory(tertiarygroup)
        donation_factory(sibling_tertiarygroup)

        response = self.auth_get(client, user=tertiarygroup_user)

        assert response.status_code == 200
        assert [item['id'] for item in response.json()[self.items_key]] == [own.id]

    def test_list_shows_every_tertiarygroup_of_the_user_regional(
        self,
        client,
        regional_user,
        tertiarygroup,
        sibling_tertiarygroup,
        foreign_tertiarygroup,
        donation_factory,
    ):
        donation_factory(tertiarygroup)
        donation_factory(sibling_tertiarygroup)
        donation_factory(foreign_tertiarygroup)

        response = self.auth_get(client, user=regional_user)

        assert response.json()['count'] == 2

    def test_list_filters_by_status(
        self, client, tertiarygroup_user, tertiarygroup, donation_factory
    ):
        paid = donation_factory(tertiarygroup, status=DonationStatus.PAID)
        donation_factory(tertiarygroup)

        response = self.auth_get(client, user=tertiarygroup_user, params={'status': 'paid'})

        assert [item['id'] for item in response.json()[self.items_key]] == [paid.id]

    def test_get_donation_returns_its_fields(
        self, client, tertiarygroup_user, tertiarygroup, donation_factory
    ):
        donation = donation_factory(tertiarygroup)

        response = self.auth_get(client, user=tertiarygroup_user, obj=donation)

        assert response.status_code == 200
        assert response.json() | {'created_at': None, 'updated_at': None} == {
            'id': donation.id,
            'tertiarygroup': {'id': tertiarygroup.id, 'name': tertiarygroup.name},
            'donor_name': 'Maria',
            'amount': '50.00',
            'method': 'pix',
            'status': 'pending',
            'created_at': None,
            'updated_at': None,
        }

    def test_get_donation_outside_scope_returns_404(
        self, client, tertiarygroup_user, sibling_tertiarygroup, donation_factory
    ):
        donation = donation_factory(sibling_tertiarygroup)

        response = self.auth_get(client, user=tertiarygroup_user, obj=donation)

        assert response.status_code == 404

    def test_create_donation(self, client, tertiarygroup_user, tertiarygroup):
        body = {
            'tertiarygroup_id': tertiarygroup.id,
            'donor_name': 'Maria',
            'amount': '50.00',
            'method': 'pix',
        }

        response = self.auth_post(client, user=tertiarygroup_user, body=body)

        assert response.status_code == 201
        assert response.json()['status'] == 'pending'

    def test_create_donation_rejects_non_positive_amount(
        self, client, tertiarygroup_user, tertiarygroup
    ):
        body = {
            'tertiarygroup_id': tertiarygroup.id,
            'donor_name': 'Maria',
            'amount': '0',
            'method': 'pix',
        }

        response = self.auth_post(client, user=tertiarygroup_user, body=body)

        assert response.status_code == self.validation_status_code

    def test_create_donation_rejects_tertiarygroup_outside_scope(
        self, client, tertiarygroup_user, sibling_tertiarygroup
    ):
        body = {
            'tertiarygroup_id': sibling_tertiarygroup.id,
            'donor_name': 'Maria',
            'amount': '50.00',
            'method': 'pix',
        }

        response = self.auth_post(client, user=tertiarygroup_user, body=body)

        assert response.status_code == 400
        assert response.json() == {'detail': 'Church not found in your scope.'}

    def test_cancel_pending_donation(
        self, client, tertiarygroup_user, tertiarygroup, donation_factory
    ):
        donation = donation_factory(tertiarygroup)

        response = self.auth_post(
            client, user=tertiarygroup_user, uri=f'{self.base_uri}{donation.id}/cancel/'
        )

        assert response.status_code == 200
        assert response.json()['status'] == 'canceled'

    def test_cancel_paid_donation_returns_409(
        self, client, tertiarygroup_user, tertiarygroup, donation_factory
    ):
        donation = donation_factory(tertiarygroup, status=DonationStatus.PAID)

        response = self.auth_post(
            client, user=tertiarygroup_user, uri=f'{self.base_uri}{donation.id}/cancel/'
        )

        assert response.status_code == 409
        assert response.json() == {'detail': 'Only pending donations can be canceled.'}


@pytest.mark.django_db
class TestNinjaDonationApi(DonationApiContract):
    base_uri = '/ninja/v1/donation/'
    items_key = 'items'
    validation_status_code = 422


@pytest.mark.django_db
class TestDrfDonationApi(DonationApiContract):
    base_uri = '/drf/v1/donation/'
    items_key = 'results'
    validation_status_code = 400
