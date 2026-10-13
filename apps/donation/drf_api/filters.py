import django_filters as filters

from apps.donation.models import Donation


class DonationFilter(filters.FilterSet):
    tertiarygroup_id = filters.NumberFilter(field_name='tertiarygroup_id')

    class Meta:
        model = Donation
        fields = ['status', 'method']
