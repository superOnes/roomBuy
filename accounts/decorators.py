from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect, resolve_url
from django.core.urlresolvers import reverse


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
            if request.user.is_admin is True:
                return func(request, *args, **kwargs)
        print(request.get_full_path())
        return redirect('/acc/login/?next=%s' % request.get_full_path())
    return return_wrapper
