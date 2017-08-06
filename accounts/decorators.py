from functools import wraps
from datetime import datetime, timedelta

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import redirect

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
        event = Event.get(eventid)
        now = datetime.now()
        if not event.is_pub:
            logout(request)
            return JsonResponse({'response_state': 403, 'msg': '活动还未推出！'})
        if (now < event.test_start + timedelta(hours=-0.5) or (now > event.test_end and now <
                                       event.event_start + timedelta(hours=-0.5)) or now > event.event_end):
            return JsonResponse({'response_state': 401, 'msg': '不在活动登录期间！'})
        if not request.user.is_authenticated() or request.user.is_admin:
            return JsonResponse({'response_state': 401, 'msg': '请登录！'})
        return func(request, *args, **kwargs)
    return wrapper


def customer_login_time(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        eventid = request.GET.get('id', request.POST.get('id'))
        event = Event.get(eventid)
        now = datetime.now()
        if now < event.test_start or now < event.event_start:
            return JsonResponse({'response_state': 405, 'msg': '活动还未正式开始！'})
        return func(request, *args, **kwargs)
    return wrapper
