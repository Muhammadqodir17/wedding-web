from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError


def is_valid_tokens(refresh_token, access_token):
    try:
        RefreshToken(refresh_token)
        AccessToken(access_token)
        return True
    except TokenError:
        return False