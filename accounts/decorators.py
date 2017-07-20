import time
from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect, resolve_url
from django.core.urlresolvers import reverse
from .models import Customer


RETURN_JSON = 1
RETURN_PAGE = 2


def superadmin_required(return_type=RETURN_JSON):
    def func_wrapper(func):
        @wraps(func)
        def return_wrapper(request, *args, **kwargs):
            response = JsonResponse({'success': False, 'msg': '您未拥有此权限'})
            if return_type == RETURN_PAGE:
                response = redirect('/')
            if request.user.is_authenticated():
                if request.user.is_superuser:
                    return func(request, *args, **kwargs)
            return response
        return return_wrapper
    return func_wrapper


def admin_required(func):
    @wraps(func)
    def return_wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            if request.user.is_admin:
                return func(request, *args, **kwargs)
        return redirect('/acc/login/?next=%s' % request.get_full_path())
    return return_wrapper


def customer_login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            if not request.user.is_admin:
                return func(request, *args, **kwargs)
        return JsonResponse({'response_state': 403})
    return wrapper


def customer_login_time(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        if time.strftime('%Y%m%d %H:%M:%S') <= user.customer.event.event_end.strftime('%Y%m%d %H:%M:%S'):
            if time.strftime('%Y%m%d %H:%M:%S') <= user.customer.event.event_start.strftime('%Y%m%d %H:%M:%S'):
                return JsonResponse({'response_state': 403})
            else:
                return func(request, *args, **kwargs)
        else:
            return JsonResponse({'response_state': 403})
    return wrapper


def login_time(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        mobile = request.POST.get('tel')
        identication = request.POST.get('personId')
        try:
            customer = Customer.objects.get(
                mobile=mobile, identication=identication)
        except BaseException:
            return JsonResponse({'response_state': 400})
        else:
            if time.strftime('%Y%m%d %H:%M:%S') <= customer.event.event_end.strftime('%Y%m%d %H:%M:%S'):
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({'response_state': 403})
    return wrapper

