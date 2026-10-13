from drf_spectacular.utils import extend_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.donation.drf_api.filters import DonationFilter
from apps.donation.drf_api.serializers import DonationCreateSerializer, DonationSerializer
from apps.donation.models import Donation
from apps.donation.services.donation_service import DonationService
from misc.drf.mixins import UserScopedQuerysetMixin


@extend_schema(tags=['donation'])
class DonationViewSet(
    UserScopedQuerysetMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Donation.objects.select_related('tertiarygroup').order_by('-created_at')
    serializer_class = DonationSerializer
    filterset_class = DonationFilter

    @extend_schema(summary='List donations')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary='Get a donation')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary='Register a donation',
        request=DonationCreateSerializer,
        responses={201: DonationSerializer},
    )
    def create(self, request):
        serializer = DonationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        donation = DonationService.create_donation(user=request.user, **serializer.validated_data)
        return Response(DonationSerializer(donation).data, status=status.HTTP_201_CREATED)

    @extend_schema(summary='Cancel a pending donation', request=None)
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        donation = DonationService.cancel_donation(self.get_object())
        return Response(self.get_serializer(donation).data)
