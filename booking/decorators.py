from accounts.models import User
from django.shortcuts import redirect, HttpResponse


def is_super_user(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        try:
            if request.user not in User.objects.filter(is_superuser=True):
                 return redirect("booking")
            
        except User.DoesNotExist:
            pass
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func
