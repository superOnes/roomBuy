from functools import wraps
from datetime import datetime

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect

from django.contrib.sessions.models import Session
from apt.models import Event


RETURN_JSON = 1
RETURN_PAGE = 2


def admin_required(func):
    @wraps(func)
    def return_wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.is_admin:
                if request.user.expire_date is None \
                   or request.user.expire_date > datetime.now():
                    return func(request, *args, **kwargs)
            logout(request)
        return redirect('/acc/login/?next=%s' % request.get_full_path())
    return return_wrapper


def customer_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        eventid = request.GET.get('id', request.POST.get('id'))
        key = request.GET.get('key', request.POST.get('key'))
        if not Event.get(eventid).is_pub:
            logout(request)
            return JsonResponse({'response_state': 403, 'msg': '活动已经下架！'})
        try:
            Session.objects.get(pk=key)
        except:
            return JsonResponse({'response_state': 403, 'msg': '请登录！'})
        else:
            return func(request, *args, **kwargs)
    return wrapper
