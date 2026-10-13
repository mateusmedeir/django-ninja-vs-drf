from django.shortcuts import get_object_or_404
from ninja import Query, Router, Status
from ninja.pagination import LimitOffsetPagination, paginate

from apps.donation.models import Donation
from apps.donation.ninja_api.filters import DonationFilterSchema
from apps.donation.ninja_api.schemas import DonationIn, DonationOut
from apps.donation.services.donation_service import DonationService
from misc.ninja.schemas import ErrorResponse

router = Router(tags=['donation'])


@router.get('/', response=list[DonationOut], summary='List donations')
@paginate(LimitOffsetPagination)
def list_donations(request, filters: Query[DonationFilterSchema]):
    donations = Donation.objects.visible_to(request.auth).select_related('tertiarygroup')
    return filters.filter(donations).order_by('-created_at')


@router.get(
    '/{donation_id}/', response={200: DonationOut, 404: ErrorResponse}, summary='Get a donation'
)
def get_donation(request, donation_id: int):
    donations = Donation.objects.visible_to(request.auth).select_related('tertiarygroup')
    return get_object_or_404(donations, id=donation_id)


@router.post('/', response={201: DonationOut, 400: ErrorResponse}, summary='Register a donation')
def create_donation(request, payload: DonationIn):
    donation = DonationService.create_donation(user=request.auth, **payload.model_dump())
    return Status(201, donation)


@router.post(
    '/{donation_id}/cancel/',
    response={200: DonationOut, 404: ErrorResponse, 409: ErrorResponse},
    summary='Cancel a pending donation',
)
def cancel_donation(request, donation_id: int):
    donations = Donation.objects.visible_to(request.auth).select_related('tertiarygroup')
    donation = get_object_or_404(donations, id=donation_id)
    return DonationService.cancel_donation(donation)
