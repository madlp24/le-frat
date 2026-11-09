"""Project middleware."""

from django.conf import settings


class DefaultLanguageMiddleware:
    """Serve Spanish by default, whatever the browser asks for.

    LocaleMiddleware falls back to the Accept-Language header before
    LANGUAGE_CODE, so a visitor with an English browser landed on the
    English site. Le Frat is a Bogota restaurant: Spanish is the default
    and English is a choice. Once someone picks a language with the
    switcher the cookie is set and we leave their choice alone.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.LANGUAGE_COOKIE_NAME not in request.COOKIES:
            request.META["HTTP_ACCEPT_LANGUAGE"] = settings.LANGUAGE_CODE
        return self.get_response(request)
