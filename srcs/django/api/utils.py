from user.models import User

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from django.forms.models import model_to_dict
from django.http import JsonResponse


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, User):
            return {
                "id": o.pk,
                "username": o.username,
                "email": o.email,
            }
        if isinstance(o, Model):
            return model_to_dict(o)
        return super().default(o)


class JsendResponse(JsonResponse):
    def __init__(self, data, message=None, status=200, **kwargs):
        super().__init__(
            {
                "status": "success" if status == 200 else "fail",
                "data": data,
                "message": message,
            },
            encoder=ExtendedEncoder,
            status=status,
            **kwargs,
        )
