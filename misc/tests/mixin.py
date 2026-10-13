import json

from apps.user.models import AccessToken


class AuthRequestMixin:
    base_uri: str = ''

    def auth_get(self, client, user=None, obj=None, params=None, uri=None):
        return client.get(self._get_uri(obj, uri), params, **self._get_headers(user))

    def auth_post(self, client, user=None, body=None, uri=None):
        return client.post(
            uri or self.base_uri,
            json.dumps(body or {}),
            content_type='application/json',
            **self._get_headers(user),
        )

    def _get_uri(self, obj, uri):
        if uri:
            return uri
        return f'{self.base_uri}{obj.id}/' if obj else self.base_uri

    @staticmethod
    def _get_headers(user):
        if not user:
            return {}
        token, _ = AccessToken.objects.get_or_create(user=user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token.key}'}
