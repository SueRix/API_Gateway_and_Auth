from functools import wraps
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        jwt_authentication = JSONWebTokenAuthentication()

        try:
            auth = jwt_authentication.authenticate(request)
            if not auth:
                raise AuthenticationFailed('No such token.')

            request.user, request.token = auth

        except AuthenticationFailed as e:
            return JsonResponse({'detail': str(e)}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
