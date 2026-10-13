from decimal import Decimal

from rest_framework import serializers

from apps.donation.choices import DonationMethod
from apps.donation.models import Donation
from apps.group.models import TertiaryGroup


class TertiaryGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TertiaryGroup
        fields = ['id', 'name']


class DonationCreateSerializer(serializers.Serializer):
    tertiarygroup_id = serializers.IntegerField()
    donor_name = serializers.CharField(min_length=1, max_length=120)
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    method = serializers.ChoiceField(choices=DonationMethod.choices)


class DonationSerializer(serializers.ModelSerializer):
    tertiarygroup = TertiaryGroupSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = [
            'id',
            'tertiarygroup',
            'donor_name',
            'amount',
            'method',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields
