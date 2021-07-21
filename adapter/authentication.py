# Source: https://gist.github.com/cb109/c81bb35ed3dcfe093d5a5775f31e2ea2

from datetime import timedelta
from TinkoffAdapter.settings import TOKEN_EXPIRED_AFTER_SECONDS
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class ExpTokenAuthentication(TokenAuthentication):

    def is_token_expired(token):
        min_age = timezone.now() - timedelta(
            seconds=TOKEN_EXPIRED_AFTER_SECONDS)
        return token.created < min_age

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid token")

        if not token.user.is_active:
            raise AuthenticationFailed("User inactive or deleted")

        expired = ExpTokenAuthentication.is_token_expired(token)
        if expired:
            token.delete()
            # Token.objects.create(user=token.user) #  Можно сразу создавать новый токен
            raise AuthenticationFailed("Invalid token")

        return (token.user, token)
