import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from .models import BlacklistedAccessToken


class BlacklistAccessTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
            if BlacklistedAccessToken.objects.filter(token=access_token).exists():
                return JsonResponse(
                    data={'detail': 'Access token in blacklist, re-login'},
                    status=401
                )
        else:
            access_token = None


class CheckAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/rosetta/') or request.path.startswith('/admin/'):
            return None

        token = request.headers.get('Authorization')

        path = request.path
        if path.startswith('/api/v1/dashboard'):
            if token is None or len(token.split()) != 2 or token.split()[0] != 'Bearer':
                return JsonResponse(data={'error': 'unauthorized'}, status=401)
            payload = jwt.decode(token.split()[1], settings.SECRET_KEY, algorithms=['HS256'])
            if payload.get('role') != 'admin':
                return JsonResponse(data={'error': 'Permission denied'}, status=403)

from django.utils import translation
from django.conf import settings

class ForceDefaultLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        translation.activate(settings.LANGUAGE_CODE)
        request.LANGUAGE_CODE = settings.LANGUAGE_CODE
        response = self.get_response(request)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, settings.LANGUAGE_CODE)
        return response