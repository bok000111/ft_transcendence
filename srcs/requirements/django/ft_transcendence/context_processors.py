from django.conf import settings


def settings_context(request):
    return {
        'DEBUG': settings.DEBUG,
        'STATIC_URL': settings.STATIC_URL,
        'API_URL': settings.API_URL,
        'WS_URL': settings.WS_URL,
    }
