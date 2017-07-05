
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import QueryDict
from django.shortcuts import redirect
from django.contrib import messages

from .models import User
from .decorators import superadmin_required


class LoginView(View):
    '''
    登录
    '''

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://www.baidu.com')
        else:
            messages.error(request, '用户名或密码错误')


@method_decorator(superadmin_required(), name='dispatch')
class UserListView(View):
    '''
    用户参数
    '''

    def get(self, request, *args, **kwargs):
        queryset = User.all()
        user_list = [{
            'id': user.id,
            'username': user.username,
        } for user in queryset]
        context = {}
        context['objects'] = user_list
        return JsonResponse(context)


@method_decorator(superadmin_required(), name='dispatch')
class UserConfigView(View):
    '''
    注册
    '''

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.filter(username=username)
            if user:
                return JsonResponse({'success': False, 'msg': '用户名已存在'})
            else:
                User.objects.create_user(
                    username=username,
                    password=password1,
                )
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'msg': '两次密码输入不一致，请重新输入！'})

    '''
     更改用户信息
     '''

    def put(self, request, *args, **kwargs):
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        username = put.get('username')
        if id:
            user = User.get(id)
            user.username = username
            user.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})

    '''
    删除账户
    '''

    def delete(self, request):
        params = QueryDict(request.body, encoding=request.encoding)
        User.remove(params.get('id'))
        return JsonResponse({'success': True})


@method_decorator(superadmin_required(), name='dispatch')
class PasswordResetView(View):
    '''
    密码重置
    '''

    def put(self, request):
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        if id:
            user = User.get(id)
            user.set_password(111111)
            user.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'msg': '用户不存在'})


@method_decorator(superadmin_required(), name='dispatch')
class AccountStatusView(View):
    '''
    禁用/启用账户
    '''

    def put(self, request, *args, **kwargs):
        put = QueryDict(request.body, encoding=request.encoding)
        id = put.get('id')
        if id:
            user = User.get(id)
            user.is_active = not user.is_active
            user.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'msg': '用户不存在'})


@method_decorator(login_required, name='dispatch')
class PersonalSettingsView(View):
    '''
    用户修改个人密码
    '''

    def post(self, request, *args, **kwargs):
        user = request.user
        oldpassword = request.POST.get('oldpassword')
        newpassword1 = request.POST.get('newpassword1')
        newpassword2 = request.POST.get('newpassword2')
        user = authenticate(username=user.username, password=oldpassword)
        if user is not None:
            if newpassword1 == newpassword2:
                user.set_password(newpassword2)
                user.save()
                login(request, user)
                return JsonResponse({'success': True, 'msg': '密码修改成功！'})
            return JsonResponse({'success': False, 'msg': '两次密码输入不一致，请重新输入！'})
        return JsonResponse({'success': False, 'msg': '密码错误！'})


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    '''
    退出登录
    '''

    def post(self, request):
        logout(request)
        return JsonResponse({'success': True, 'msg': '退出登录成功'})
