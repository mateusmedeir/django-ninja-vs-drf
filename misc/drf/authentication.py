from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from apps.user.models import AccessToken


class BearerTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        scheme, _, token = get_authorization_header(request).decode().partition(' ')
        if scheme != self.keyword or not token:
            return None

        access_token = AccessToken.objects.select_related('user').filter(key=token).first()
        if not access_token:
            raise AuthenticationFailed('Invalid token.')

        return access_token.user, token

    def authenticate_header(self, request):
        return self.keyword


class BearerTokenScheme(OpenApiAuthenticationExtension):
    target_class = BearerTokenAuthentication
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='AUTHORIZATION', token_prefix=BearerTokenAuthentication.keyword
        )
