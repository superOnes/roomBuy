import os
import xlrd
import uuid
from datetime import datetime, timedelta

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.sessions.models import Session

from apt.models import Event, EventDetail
from aptm import settings
from .models import User, Customer, Order
from .decorators import customer_login_time


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
                if user.expire_date is None \
                   or user.expire_date > datetime.now():
                    login(request, user)
                    return redirect(nxt)
        messages.error(request, '用户名或密码不正确')
        return redirect(reverse('acc_login'))


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

    def post(self, request):
        mobile = request.POST.get('tel')
        identication = request.POST.get('personId')
        eventid = request.POST.get('id')
        event = Event.get(eventid)
        now = datetime.now()
        if event.is_pub:
            if (now < event.test_start + timedelta(hours=-0.5) or (now > event.test_end and now < event.event_start +
                                   timedelta(hours=-0.5)) or now > event.event_end):
                return JsonResponse(
                    {'response_state': 400, 'msg': '不在活动登录期间！'})
            try:
                customer = Customer.objects.get(
                    mobile=mobile, identication=identication, event_id=eventid)
            except BaseException:
                return JsonResponse(
                    {'response_state': 400, 'msg': '用户名或密码不正确！'})
            else:
                session_key = customer.session_key
                user = authenticate(
                    username=customer.user.username,
                    password=customer.identication)
                if user:
                    if not user.is_admin:
                        login(request, user)
                        request.session.set_expiry(300)
                        value = [{
                            'termname': customer.event.termname,
                            'term': customer.event.term,
                        }]
                        if session_key:
                            Session.objects.filter(pk=session_key).delete()
                            customer.session_key = request.session.session_key
                            customer.save()
                            return JsonResponse(
                                {'response_state': 200, 'msg': '登录成功', 'objects': value})
                        else:
                            customer.session_key = request.session.session_key
                            customer.save()
                            return JsonResponse(
                                {'response_state': 200, 'msg': '登录成功', 'objects': value})
                    return JsonResponse({'response_state': 400})
                return JsonResponse(
                    {'response_state': 400, 'msg': '该电话号与证件号不匹配！'})
        return JsonResponse({'response_state': 403, 'msg': '活动还未正式推出！'})


# @method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class CustomerLogoutView(View):
    '''
    顾客退出登录
    '''

    def post(self, request):
        user = request.user
        user.customer.session_key = None
        user.customer.save()
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
            filename = file.name.split('.')[-1]
            if filename == 'xlsx' or filename == 'xls':
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
                num = 0
                for rx in range(1, row):
                    li = []
                    for cx in range(0, col):
                        value = sheet.cell(rowx=rx, colx=cx).value
                        li.append(value)
                    data.append(li)
                for ct in data:
                    if type(ct[1]) != str:
                        ct[1] = str(int(ct[1]))
                    if type(ct[2]) != str:
                        ct[2] = str(int(ct[2]))
                    if (Customer.objects.filter(event_id=id,
                                                mobile=ct[1]) or Customer.objects.filter(event_id=id,
                                                                                                   identication=ct[2])).exists():
                        continue
                    else:
                        with transaction.atomic():
                            customer = Customer.objects.create(realname=ct[0],
                                                               mobile=ct[1],
                                                               identication=ct[2],
                                                               remark=ct[3],
                                                               event=event)
                            customer.save()
                            User.objects.create_user(
                                username=uuid.uuid1(),
                                password=customer.identication,
                                customer=customer,
                                is_admin=False)
                            num += 1
                return JsonResponse({'success': True, 'data': num})
            else:
                return JsonResponse({'success': False, 'msg': '导入文件格式不正确！'})
        os.remove('media/tmp/customer.xlsx')
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
                                     'msg': '该用户已备注或已购买，不可备注'})
            return JsonResponse({'response_state': 200, 'result': result})
        return JsonResponse({'response_state': 300, 'msg': '未找到相关用户'})
