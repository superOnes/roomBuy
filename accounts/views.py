import os
import xlrd
import uuid
import time
from collections import Counter

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.generic import View, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, QueryDict
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction

from apt.models import Event, EventDetail
from aptm import settings
from .models import User, Customer, Order
from .decorators import superadmin_required, login_time, customer_login_required


class LoginView(View):
    '''
    登录
    '''

    def get(self, request):
        return render(request, 'index.html', {'next': request.GET.get('next')})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        nxt = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_admin:
                login(request, user)
                return redirect(nxt)
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


# @method_decorator(login_time, name='dispatch')
class CustomerLoginView(View):
    '''
    顾客登录
    '''

    def post(self, request):
        userid=request.POST.get('userid')
        customer=User.get(userid).customer
        # try:
        #     request.session[time.strftime("%Y%m%d%H%M%S")] = customer.realname + \
        #         customer.mobile + customer.identication
        #     count = Counter(
        #         request.session.values()).get(
        #         customer.realname +
        #         customer.mobile +
        #         customer.identication)
        # except BaseException:
        #     return JsonResponse({'response_state': 400, 'msg': '认筹名单中没有此用户！'})
        # else:
        userobj = customer.user
        if customer.event.is_pub:
            eventid = customer.event_id
            user = authenticate(
                username=userobj.username,
                password=customer.identication)
            if user:
                if not user.is_admin:
                    # if count > Event.get(eventid).equ_login_num:
                    #     return JsonResponse(
                    #         {'response_state': 402, 'msg': '帐号同时在线数量超出限制！'})
                    # else:
                    login(request, user)
                    request.session.set_expiry(300)
                    return JsonResponse({'response_state': 200, 'id': eventid, 'userid': user.id, 'msg': '登录成功'})
                return JsonResponse({'response_state': 400})
            return JsonResponse({'response_state': 400, 'msg': '该电话号与证件号未通过认证。'})
        return JsonResponse({'response_state': 400, 'msg': '活动还未正式推出。'})


# @method_decorator(customer_login_required, name='dispatch')
class CustomerLogoutView(View):
    '''
    顾客退出登录
    '''

    def post(self, request):
        logout(request)
        return JsonResponse({'response_state': 200, 'msg': '退出成功'})


@method_decorator(login_required, name='dispatch')
class DeleteTestView(View):
    '''
    清除公测订单
    '''

    def post(self, request):
        id = request.POST.get('id')
        eventdetail = EventDetail.objects.filter(event_id=id)
        if eventdetail:
            for ed in eventdetail:
                Order.objects.filter(eventdetail=ed,
                                     is_test=True).delete()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@method_decorator(login_required, name='dispatch')
class ImportView(View):
    '''
    导入认筹名单
    '''

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
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
                if Customer.objects.filter(event_id=id, mobile=ct[1]).exists():
                    continue
                else:
                    with transaction.atomic():
                        customer = Customer.objects.create(realname=ct[0],
                                                           mobile=str(int(ct[1])),
                                                           identication=str(int(ct[2])),
                                                           remark=ct[3],
                                                           event=event)
                        customer.save()
                        User.objects.create_user(
                            username=uuid.uuid1(),
                            password=customer.identication,
                            customer=customer,
                            is_admin=False)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


class GetCustomerInfo(View):
    def get(self, request):
        identication = request.GET.get('id')
        event_id = request.GET.get('eid')
        customer = Customer.get_by_event(event_id, identication)
        if customer:
            result = {
                'id': customer.id,
                'realname': customer.realname,
                'mobile': customer.mobile,
                'identication': customer.identication,
            }
            if customer.user.order_set.count() >= customer.count:
                return JsonResponse({'response_state': 301,
                                     'result': result,
                                     'msg': '该用户已备注，不可再次备注'})
            return JsonResponse({'response_state': 200, 'result': result})
        return JsonResponse({'response_state': 300, 'msg': '未找到相关用户'})
