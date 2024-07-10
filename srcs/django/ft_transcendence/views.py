import os
from django.shortcuts import redirect


def index(_):
    return redirect(f"https://{os.getenv('HOST_NAME')}")
