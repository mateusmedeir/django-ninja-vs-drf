from ninja.security import HttpBearer

from apps.user.models import AccessToken


class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        access_token = AccessToken.objects.select_related('user').filter(key=token).first()
        return access_token.user if access_token else None
