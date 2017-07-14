import os
import xlrd
import uuid

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import QueryDict
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse

from apt.models import Event
from aptm import settings
from .models import User, Customer, Order
from .decorators import superadmin_required


class LoginView(View):
    '''
    登录
    '''

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_admin:
                login(request, user)
                return redirect('/event/list/')
        messages.error(request, '用户名或密码不正确')
        return redirect(reverse('acc_login'))


@method_decorator(superadmin_required(), name='dispatch')
class UserListView(ListView):
    '''
    后台用户列表
    '''
    model = User
    template_name = 'userlist.html'
    fields = ['username', 'password', 'is_delete']

    def get_queryset(self):
        return self.model.objects.filter(is_admin=True).order_by('-id')


@method_decorator(superadmin_required(), name='dispatch')
class UserConfigView(View):
    '''
    注册后台用户
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
                    is_admin=True,
                )
                return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'msg': '两次密码输入不一致，请重新输入！'})

    '''
     更改后台用户信息
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
    删除用户
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


class CustomerLoginView(View):
    '''
    顾客登录
    '''

    def post(self, request, *args, **kwargs):
        mobile = request.POST.get('tel')
        identication = request.POST.get('personId')
        response = JsonResponse({'response_state': 400})
        response['Access-Control-Allow-Origin'] = '*'
        try:
            customer = Customer.objects.get(
                mobile=mobile, identication=identication)
        except BaseException:
            return response
        else:
            userobj = customer.user
            eventid = customer.event_id
            user = authenticate(
                username=userobj.username,
                password=identication)
            if user:
                if not user.is_admin:
                    login(request, user)
                    response = JsonResponse(
                        {'response_state': 200, 'id': eventid})
                    response['Access-Control-Allow-Origin'] = '*'
                    return response
                return response
            return response

class DeleteTestView(View):
    '''
    清除公测订单
    '''

    def post(self, request):
        id = request.POST.get('id')
        Order.objects.filter(event_id=id).delete()
        return JsonResponse({'success': False})


class ImportView(View):
    '''
    导入认筹名单
    '''

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        # custom = Customer.objects.filter(event_id=id)
        if id:
            event = Event.get(id)
            file = request.FILES.get('filename')
            path = default_storage.save(
                'tmp/customer.xlsx',
                ContentFile(
                    file.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            workdata = xlrd.open_workbook(tmp_file)
            sheet_name = workdata.sheet_names()[0]
            sheet = workdata.sheet_by_name(sheet_name)
            row = sheet.nrows
            col = sheet.ncols
            data = []
            for rx in range(1, row):
                li = []
                for cx in range(0, col):
                    value = sheet.cell(rowx=rx, colx=cx).value
                    li.append(value)
                data.append(li)
            for ct in data:
                if Customer.objects.all(event_id=id, mobile=ct[1]).exists():
                    continue
                else:
                    customer = Customer.objects.create(realname=ct[0],
                                                       mobile=ct[1],
                                                       identication=ct[2],
                                                       remark=ct[3],
                                                       event=event)
                    customer.save()
                    User.objects.create_user(username=uuid.uuid1(),
                                             password=customer.identication,
                                             customer=customer,
                                             is_admin=False)
                    return JsonResponse({'success': True})
        return JsonResponse({'success': False})
