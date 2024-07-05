from time import perf_counter
from importlib import import_module
from contextlib import contextmanager
from channels.db import database_sync_to_async
from django.conf import settings
from django.http import HttpRequest, SimpleCookie


def _login(user, backend=None):
    from django.contrib.auth import login

    engine = import_module(settings.SESSION_ENGINE)
    request = HttpRequest()
    request.session = engine.SessionStore()
    login(request, user, backend)
    # Save the session values.
    request.session.save()
    # Create a cookie to represent the session.
    session_cookie = settings.SESSION_COOKIE_NAME
    cookies = SimpleCookie()
    cookies[session_cookie] = request.session.session_key
    cookie_data = {
        "max-age": None,
        "path": "/",
        "domain": settings.SESSION_COOKIE_DOMAIN,
        "secure": settings.SESSION_COOKIE_SECURE or None,
        "expires": None,
    }
    cookies[session_cookie].update(cookie_data)
    return cookies


@database_sync_to_async
def login(**credentials):
    from django.contrib.auth import authenticate

    user = authenticate(**credentials)
    if user:
        return _login(user)

    return SimpleCookie()


@database_sync_to_async
def logout(cookies):
    """Log out the user by removing the cookies and session object."""
    from django.contrib.auth import logout

    engine = import_module(settings.SESSION_ENGINE)
    session_cookie = cookies.get(settings.SESSION_COOKIE_NAME)
    request = HttpRequest()
    session_key = session_cookie.value
    request.session = engine.SessionStore(session_key)
    logout(request)
    return SimpleCookie()


@contextmanager
def timer(name: str = ""):
    start = perf_counter()
    end = None
    try:
        yield lambda: (perf_counter() - start) if end is None else (end - start)
    finally:
        end = perf_counter()
        print(f"{name} took {end - start:.6f} seconds")
