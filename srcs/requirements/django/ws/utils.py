from functools import wraps
from inspect import iscoroutinefunction


def ws_need_auth(consumer):
    if iscoroutinefunction(consumer):

        @wraps(consumer)
        async def _wrapped_view(self, *args, **kwargs):
            if not self.scope["user"].is_authenticated:
                await self.close(code=403, reason="User is not authenticated")
                return
            return await consumer(self, *args, **kwargs)

        return _wrapped_view

    else:

        @wraps(consumer)
        def _wrapped_view(self, *args, **kwargs):
            if not self.scope["user"].is_authenticated:
                self.close(code=403, reason="User is not authenticated")
                return
            return consumer(self, *args, **kwargs)

        return _wrapped_view
