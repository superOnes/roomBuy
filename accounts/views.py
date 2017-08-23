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


from apt.models import Event, EventDetail
from aptm import settings
from .models import User, Customer, Order
from .decorators import admin_required


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
                if user.company.expire_date is None \
                   or user.company.expire_date > datetime.now():
                    login(request, user)
                return redirect(nxt)
        messages.error(request, '用户名或密码不正确')
        return redirect(reverse('acc_login'))


@method_decorator(login_required, name='dispatch')
class PersonalSettingsView(View):
    '''
    用户修改个人密码
    '''

    def post(self, request):
        user = request.user
        if user.is_admin and not user.is_delete:
            oldpassword = request.POST.get('oldpassword')
            user = authenticate(username=user.username, password=oldpassword)
            if user:
                newpassword1 = request.POST.get('newpassword1')
                newpassword2 = request.POST.get('newpassword2')
                if newpassword1 == newpassword2:
                    user.set_password(newpassword2)
                    user.save()
                    login(request, user)
                    return JsonResponse(
                        {'response_state': 200, 'msg': '密码修改成功'})
                return JsonResponse(
                    {'response_state': 400, 'msg': '两次新密码输入不一致'})
            return JsonResponse({'response_state': 400, 'msg': '原密码输入错误'})
        return JsonResponse({'response_state': 400, 'msg': '您不是管理员用户'})


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
            if (now < event.test_start + timedelta(hours=-0.5)
                or (event.test_end < now < event.event_start + timedelta(hours=-0.5))
                    or now > event.event_end):
                return JsonResponse(
                    {'response_state': 400, 'msg': '不在活动登录期间！'})
            try:
                customer = Customer.objects.get(
                    mobile=mobile, identication=identication, event_id=eventid)
            except BaseException:
                return JsonResponse(
                    {'response_state': 400, 'msg': '用户名或密码不正确！'})
            else:
                if customer.user:
                    if not customer.user.is_admin:
                        value = [{
                            'termname': customer.event.termname,
                            'term': customer.event.term,
                        }]
                        return JsonResponse(
                            {'response_state': 200, 'objects': value})
                    return JsonResponse({'response_state': 400})
                return JsonResponse(
                    {'response_state': 400, 'msg': '该电话号与证件号不正确！'})
        return JsonResponse({'response_state': 403, 'msg': '活动还未正式推出！'})


class CustomerLogoutView(View):
    '''
    顾客退出登录
    '''

    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'response_state': 400, 'msg': '您之前没登录或已经退出！'})
        user.customer.session_key = None
        user.customer.save()
        logout(request)
        return JsonResponse({'response_state': 200, 'msg': '退出成功！'})


@method_decorator(admin_required, name='dispatch')
class DeleteTestView(View):
    '''
    清除公测订单
    '''

    def post(self, request):
        id = request.POST.get('id')
        eventdetail = EventDetail.objects.filter(event_id=id)
        if eventdetail:
            for ed in eventdetail:
                order = Order.objects.filter(eventdetail=ed, is_test=True)
                for od in order:
                    od.delete()
                    ed.is_testsold = False
                    ed.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False})


@method_decorator(login_required, name='dispatch')
class ImportView(View):
    '''
    导入认筹名单
    '''

    def post(self, request, *args, **kwargs):
        id = request.POST.get('id')
        event = Event.get(id)
        file = request.FILES.get('filename')
        if not file:
            return JsonResponse({'response_state': 400, 'msg': '没有选择文件！'})
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
            if row == 0 or row == 1:
                os.remove('media/tmp/customer.xlsx')
                return JsonResponse(
                    {'response_state': 400, 'msg': '导入的excel为空表！'})
            if col != 6:
                return JsonResponse(
                    {'response_state': 400, 'msg': '导入文件不正确！'})
            value1 = sheet.cell(rowx=0, colx=0).value
            value2 = sheet.cell(rowx=0, colx=1).value
            value3 = sheet.cell(rowx=0, colx=2).value
            value4 = sheet.cell(rowx=0, colx=3).value
            value5 = sheet.cell(rowx=0, colx=4).value
            value6 = sheet.cell(rowx=0, colx=5).value
            head = [value1, value2, value3, value4, value5, value6]
            if head != ['姓名', '手机号', '证件号', '备注', '置业顾问', '顾问电话']:
                return JsonResponse(
                    {'response_state': 400, 'msg': '导入文件不正确！'})
            data = []
            for rx in range(1, row):
                value1 = sheet.cell(rowx=rx, colx=0).value
                value2 = sheet.cell(rowx=rx, colx=1).value
                value3 = sheet.cell(rowx=rx, colx=2).value
                value4 = sheet.cell(rowx=rx, colx=3).value
                value5 = sheet.cell(rowx=rx, colx=4).value
                value6 = sheet.cell(rowx=rx, colx=5).value
                if not isinstance(value1, str):
                    try:
                        value1 = str(int(value1))
                    except BaseException:
                        return JsonResponse(
                            {'response_state': 400, 'msg': '姓名格式不正确！'})
                if not isinstance(value4, str):
                    try:
                        value4 = str(int(value4))
                    except BaseException:
                        return JsonResponse(
                            {'response_state': 400, 'msg': '备注格式不正确！'})
                if not isinstance(value5, str):
                    try:
                        value5 = str(int(value5))
                    except BaseException:
                        return JsonResponse(
                            {'response_state': 400, 'msg': '置业顾问格式不正确！'})
                if not isinstance(value3, str):
                    try:
                        value3 = str(int(value3))
                    except BaseException:
                        os.remove('media/tmp/customer.xlsx')
                        return JsonResponse(
                            {'response_state': 400, 'msg': '身份证号有误！'})
                try:
                    value2 = str(int(value2))
                except BaseException:
                    os.remove('media/tmp/customer.xlsx')
                    return JsonResponse(
                        {'response_state': 400, 'msg': '导入手机号格式有误！'})
                if value6:
                    try:
                        value6 = str(int(value6))
                    except BaseException:
                        os.remove('media/tmp/customer.xlsx')
                        return JsonResponse(
                            {'response_state': 400, 'msg': '导入顾问电话格式有误！'})
                li = [value1, value2, value3, value4, value5, value6]
                data.append(li)
            realname = list(map(lambda x: (x[0]), data))
            for rl in realname:
                rl = str(rl).replace(' ', '')
                if len(rl) == 0:
                    return JsonResponse(
                        {'response_state': 400, 'msg': '姓名,手机号，证件号不能为空！'})
            mobile = list(map(lambda x: (x[1]), data))
            if len(set(mobile)) < len(mobile):
                os.remove('media/tmp/customer.xlsx')
                return JsonResponse(
                    {'response_state': 400, 'msg': '手机号有重复，请查询后重试！'})
            identification = list(map(lambda x: (x[2]), data))
            for idt in identification:
                idt = str(idt).replace(' ', '')
                if len(idt) == 0:
                    return JsonResponse(
                        {'response_state': 400, 'msg': '姓名,手机号，证件号不能为空！'})
            if len(set(identification)) < len(identification):
                os.remove('media/tmp/customer.xlsx')
                return JsonResponse(
                    {'response_state': 400, 'msg': '身份证号有重复，请查询后重试！'})
            try:
                with transaction.atomic():
                    Customer.objects.filter(event=event).delete()
                    for ct in data:
                        customer = Customer.objects.create(
                            realname=ct[0], mobile=ct[1],
                            identication=ct[2], remark=ct[3],
                            consultant=ct[4], phone=ct[5], event=event)
                        User.objects.create_user(username=uuid.uuid1(),
                                                 customer=customer,
                                                 is_admin=False)
            except:
                os.remove('media/tmp/customer.xlsx')
                return JsonResponse({'response_state': 400,
                                     'msg': '未知错误，请联系管理员'})
            os.remove('media/tmp/customer.xlsx')
            return JsonResponse({'response_state': 200, 'data': len(data)})
        return JsonResponse({'response_state': 400, 'msg': '导入文件格式不正确'})


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
                'consultant': customer.consultant,
                'phone': customer.phone
            }
            if customer.user.order_set.filter(is_test=False).count() \
               >= customer.count:
                return JsonResponse({'response_state': 301,
                                     'result': result,
                                     'msg': '该用户已备注或已购买，不可备注'})
            return JsonResponse({'response_state': 200, 'result': result})
        return JsonResponse({'response_state': 300, 'msg': '未找到相关用户'})
