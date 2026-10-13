from ninja import NinjaAPI

from apps.donation.ninja_api.router import router as donation_router
from misc.exceptions import DomainError
from misc.ninja.auth import TokenAuth

api = NinjaAPI(
    title='Donations — Django Ninja',
    version='1.0.0',
    urls_namespace='ninja',
    auth=TokenAuth(),
)


@api.exception_handler(DomainError)
def handle_domain_error(request, exc: DomainError):
    return api.create_response(request, {'detail': str(exc)}, status=exc.status_code)


api.add_router('/donation/', donation_router)
