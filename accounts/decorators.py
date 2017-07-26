from functools import wraps
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import redirect
from django.http import QueryDict

from .models import Customer, User


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
        dict = QueryDict(request.body, encoding=request.encoding)
        userid = dict.get('userid')
        user = User.get(userid)
        if user.is_authenticated():
            if not user.is_admin:
                return func(request, *args, **kwargs)
        return redirect(
            'http://hd.edu2act.cn/app_register2/views/houseList.html?id=' + str(user.customer.event.id))
    return wrapper


def customer_login_time(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        dict = QueryDict(request.body, encoding=request.encoding)
        userid = dict.get('userid')
        user = User.get(userid)
        now = datetime.now()
        if now <= user.customer.event.event_end:
            if now <= user.customer.event.event_start:
                return JsonResponse({'response_state': 403, 'msg': '活动尚未开始'})
            else:
                return func(request, *args, **kwargs)
        else:
            return JsonResponse({'response_state': 403, 'msg': '活动已经结束'})
    return wrapper


def login_time(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        mobile = request.POST.get('tel')
        identication = request.POST.get('personId')
        try:
            customer = Customer.objects.get(
                mobile=mobile, identication=identication)
            now = datetime.now()
        except BaseException:
            return JsonResponse({'response_state': 400, 'msg': '认筹名单中没有此用户'})
        else:
            if now <= customer.event.event_end:
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({'response_state': 403, 'msg': '活动已经结束'})
    return wrapper
