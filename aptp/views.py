import time
from datetime import datetime, timedelta

from django.views.generic import View
from django.http import JsonResponse
from django.db import connection, transaction
from django.utils.decorators import method_decorator
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login

from apt.models import Event, EventDetail
from aptp.models import Follow
from accounts.models import Order, Customer
from accounts.decorators import customer_login_required, customer_login_time


# @method_decorator(customer_login_required, name='dispatch')
class ProTimeView(View):
    '''
    同意协议时间
    '''

    def post(self, request):
        protime = request.POST.get('protime')
        mobile = request.POST.get('tel')
        identication = request.POST.get('personId')
        eventid = request.POST.get('id')
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
                    if session_key:
                        Session.objects.filter(pk=session_key).delete()
                        if not user.customer.protime:
                            user.customer.protime = protime
                            user.customer.save()
                        customer.session_key = request.session.session_key
                        customer.save()
                        return JsonResponse(
                            {'response_state': 200, 'msg': '登录成功',})
                    else:
                        customer.session_key = request.session.session_key
                        customer.save()
                        return JsonResponse(
                            {'response_state': 200, 'msg': '登录成功'})
                return JsonResponse({'response_state': 400})
            return JsonResponse(
                {'response_state': 400, 'msg': '该电话号与证件号不正确！'})


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailView(View):
    '''
    显示活动
    '''

    def get(self, request):
        eventid = request.GET.get('id')
        obj = Event.get(eventid)
        plane_graph = []
        if obj.plane_graph:
            plane_graph.append(obj.plane_graph.url)
        if obj.plane_graph1:
            plane_graph.append(obj.plane_graph1.url)
        if obj.plane_graph2:
            plane_graph.append(obj.plane_graph2.url)
        if obj.plane_graph3:
            plane_graph.append(obj.plane_graph3.url)
        value = [
            {
                'test_start': (
                    obj.test_start).strftime("%Y/%m/%d %H:%M:%S"),
                'test_ent': (
                    obj.test_end).strftime("%Y/%m/%d %H:%M:%S"),
                'event_start': (
                    obj.event_start).strftime("%Y/%m/%d %H:%M:%S"),
                'event_end': (
                        obj.event_end).strftime("%Y/%m/%d %H:%M:%S"),
                'notice': obj.notice,
                'description': obj.description,
                'tip': obj.tip,
                'name': obj.name,
                'plane_graph': plane_graph,
                'phone': obj.phone_num,
            }]
        context = {}
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailListView(View):
    '''
    车位/房源 楼号列表
    '''

    def get(self, request):
        eventid = request.GET.get('id')
        eventobj = Event.get(eventid)
        context = {}
        eventdetobj = EventDetail.objects.filter(event_id=eventid)
        buildinglist = []
        for obj in eventdetobj:
            buildinglist.append((obj.building))
        value = [{
            'event_name': eventobj.name,
            'customer_count': eventobj.customer_set.count(),
            'event_start': (eventobj.event_start).strftime("%Y/%m/%d %H:%M:%S"),
            'building': sorted(list(set(buildinglist))),
        }]
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailUnitListView(View):
    '''
    车位/房源 单元列表
    '''

    def get(self, request):
        eventid = request.GET.get('id')
        building = request.GET.get('building')
        context = {}
        eventdetobj = EventDetail.objects.filter(
            building=building, event_id=eventid)
        unitlist = []
        for obj in eventdetobj:
            unitlist.append((obj.unit))
        value = [{
            'unit': sorted(list(set(unitlist)))
        }]
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
class AppEventDetailHouseListView(View):
    '''
    车位/房源 房号列表
    '''

    def get(self, request):
        eventid = request.GET.get('id')
        event = Event.get(eventid)
        now = datetime.now()
        if now < event.test_start or now < event.test_start:
            response_state = 405
        else:
            response_state = None
        building = request.GET.get('building')
        unit = request.GET.get('unit')
        context = {}
        eventdetobj = EventDetail.objects.filter(
            event_id=eventid, building=building, unit=unit)
        room_num_list = []
        for obj in eventdetobj:
            if obj.status:
                value = [{
                    'house': obj.id,
                    'floor_room_num': str(obj.floor) + '-' + str(obj.room_num),
                    'is_sold': obj.is_sold,
                    'is_testsold': obj.is_testsold,
                }]
                room_num_list.append(value)
        context['objects'] = room_num_list
        context['response_state'] = response_state
        context['response_state'] = 200
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class AppEventDetailHouseInfoView(View):
    '''
    车位/房源 详情
    '''

    def get(self, request):
        user = request.user
        house = request.GET.get('house')
        eventdetobj = EventDetail.get(house)
        eventdetobj.save()
        test = True if time.strftime('%Y%m%d %H:%M:%S') <= eventdetobj.event.test_end.strftime(
            '%Y%m%d %H:%M:%S') else False
        try:
            Follow.objects.get(user=user, eventdetail=eventdetobj)
        except BaseException:
            is_followed = False,
        else:
            is_followed = True,
        try:
            house_type = eventdetobj.house_type.name
            pic = eventdetobj.house_type.pic.url
        except BaseException:
            house_type = ''
            pic = ''
        value = [{'event': eventdetobj.event.name,
                  'realname': user.customer.realname,
                  'mobile': user.customer.mobile,
                  'identication': user.customer.identication,
                  'building_unit': eventdetobj.building + eventdetobj.unit + str(eventdetobj.floor) + '层' + str(eventdetobj.room_num),
                  'total': '***' if test and not eventdetobj.event.test_price else ((eventdetobj.area) * (eventdetobj.unit_price)),
                  'house_type': house_type,
                  'pic': pic,
                  'floor': eventdetobj.floor,
                  'area': eventdetobj.area if eventdetobj.event.covered_space else '***',
                  'unit_price': eventdetobj.unit_price if eventdetobj.event.covered_space_price else '***',
                  'looking': eventdetobj.looking,
                  'term': eventdetobj.term,
                  'is_sold': eventdetobj.is_sold,
                  'is_followed': is_followed,
                  'is_testsold': eventdetobj.is_testsold,
                  }]
        context = {}
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class AddFollow(View):
    '''
    添加收藏
    '''

    def post(self, request):
        user = request.user
        house = request.POST.get('house')
        eventid = request.POST.get('id')
        try:
            eventdetail = EventDetail.get(house)
        except BaseException:
            return JsonResponse({'response_state': 400})
        else:
            if not Follow.objects.filter(
                    user=user,
                    eventdetail=eventdetail):
                if (Follow.objects.filter(user=user, eventdetail__event_id=eventid).count(
                )) < Event.get(eventid).follow_num:
                    Follow.objects.create(user=user, eventdetail=eventdetail)
                    return JsonResponse({'response_state': 200, 'msg': '收藏成功'})
                else:
                    return JsonResponse(
                        {'response_state': 400, 'msg': '收藏数量超过限制'})
            return JsonResponse({'response_state': 400, 'msg': '您已收藏过该商品！'})


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class CancelFollow(View):
    '''
    取消收藏
    '''

    def post(self, request):
        user = request.user
        house = request.POST.get('house')
        try:
            eventdetail = EventDetail.get(house)
        except BaseException:
            return JsonResponse({'response_state': 400, 'msg': '没有该商品！'})
        else:
            follow = Follow.objects.filter(
                user=user,
                eventdetail=eventdetail)
            if not follow:
                return JsonResponse(
                    {'response_state': 400, 'msg': '没有收藏该商品！'})
            follow.delete()
            return JsonResponse(
                {'response_state': 200, 'msg': '成功取消收藏！'})


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class FollowView(View):
    '''
    用户收藏列表信息
    '''

    def get(self, request):
        user = request.user
        objs = Follow.objects.filter(
            user=user, eventdetail__event_id=request.GET.get('id'))
        context = {}
        list = []
        for obj in objs:
            value = [
                {
                    'eventdetail': (
                        obj.eventdetail.building +
                        obj.eventdetail.unit +
                        str(obj.eventdetail.floor) + '层' +
                        str(obj.eventdetail.room_num)),
                    'price': (
                        (
                            obj.eventdetail.area) *
                        (
                            obj.eventdetail.unit_price)),
                    'house': obj.eventdetail.id,
                }]
            list.append(value)
        context['objects'] = list
        context['response_state'] = 200
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class AppHouseChoiceConfirmView(View):
    '''
    订单确认
    '''

    def post(self, request):
        user = request.user
        house = request.POST.get('house')
        eventid = request.POST.get('id')
        from aptm.settings import DATABASES
        cursor = connection.cursor()
        if (DATABASES['default']['NAME'] == 'aptm'):
            cursor.execute('SELECT id,is_sold,sign_id,event_id,is_testsold,\
                            building,unit,floor,room_num FROM apt_eventdetail \
                            where id=%s FOR UPDATE' % house)
            bol = True
        else:
            cursor.execute('SELECT id,is_sold,sign_id,event_id,is_testsold,\
                            building,unit,floor,room_num FROM apt_eventdetail \
                            where id=%s' % house)
            bol = 1
        obj = cursor.fetchone()
        if obj is None:
            return JsonResponse({'response_state': 404, 'msg': '目标不存在'})
        event = Event.get(obj[3])
        now = datetime.now()
        if (now >= event.test_start) and (now <= event.test_end):
            if not obj[4]:
                with transaction.atomic():
                    purchased = Order.objects.filter(
                        user=user, eventdetail__event_id=eventid, is_test=True).count()
                    if purchased >= user.customer.count:
                        return JsonResponse({'response_state': 400,
                                             'msg': '不可再次购买'})
                    order = Order.objects.create(user=user,
                                                 eventdetail_id=obj[0],
                                                 order_num=time.strftime
                                                 ('%Y%m%d%H%M%S'))
                    cursor.execute('UPDATE apt_eventdetail set is_testsold=%s \
                                    where id=%s' % (bol, house))
                return JsonResponse(
                    {
                        'response_state': 200,
                        'room_info': ('%s-%s-%s-%s') % (obj[5],
                                                        obj[6],
                                                        obj[7],
                                                        obj[8]),
                        'limit': (
                            order.time + timedelta(
                                hours=event.limit)).strftime('%Y年%m月%d日 %H:%M:%S'),
                        'ordertime': order.time,
                        'orderid': order.id,
                    })
            elif Order.objects.filter(user=user, eventdetail_id=obj[0],
                                      is_test=True).exists():
                return JsonResponse({'response_state': 400,
                                     'msg': '已购买,不要重复购买'})
        elif (now >= event.event_start) and (now <= event.event_end):
            if not obj[1] and not obj[2]:
                with transaction.atomic():
                    purchased = Order.objects.filter(
                        user=user, eventdetail__event_id=eventid, is_test=False).count()
                    if purchased >= user.customer.count:
                        return JsonResponse({'response_state': 400,
                                             'msg': '不可再次购买'})
                    order = Order.objects.create(user=user,
                                                 eventdetail_id=obj[0],
                                                 order_num=time.strftime
                                                 ('%Y%m%d%H%M%S'),
                                                 is_test=False)
                    cursor.execute('UPDATE apt_eventdetail set is_sold=%s \
                                    where id=%s' % (bol, house))
                return JsonResponse(
                    {
                        'response_state': 200,
                        'room_info': ('%s-%s-%s-%s') % (obj[5],
                                                        obj[6],
                                                        obj[7],
                                                        obj[8]),
                        'limit': (
                            order.time + timedelta(
                                hours=event.limit)).strftime('%Y年%m月%d日 %H:%M:%S'),
                        'ordertime': order.time,
                        'orderid': order.id,
                    })
            elif not obj[1] and obj[2]:
                cursor.execute(
                    'UPDATE apt_eventdetail set is_sold=%s where id=%s' %
                    (bol, house))
                return JsonResponse(
                    {'response_state': 400, 'msg': '购买失败，房屋已卖出'})
            elif Order.objects.filter(user=user, eventdetail_id=obj[0],
                                      is_test=False).exists():
                return JsonResponse({'response_state': 400,
                                     'msg': '已购买,不要重复购买'})
        return JsonResponse({'response_state': 400, 'msg': '购买失败'})


class AppHouseChoiceConfirmTestView(View):
    '''
    订单确认测试接口
    '''

    def post(self, request):
        house = request.POST.get('house')
        userid = request.POST.get('userid')
        eventid = request.POST.get('id')
        from accounts.models import User
        user = User.get(userid)
        cursor = connection.cursor()
        cursor.execute('SELECT id,is_sold,sign_id,event_id,is_testsold,\
                        building,unit,floor,room_num FROM apt_eventdetail \
                        where id=%s FOR UPDATE' % house)
        obj = cursor.fetchone()
        if obj is None:
            return JsonResponse({'response_state': 404, 'msg': '目标不存在'})
        event = Event.get(obj[3])
        now = datetime.now()
        if (now >= event.test_start) and (now <= event.test_end):
            if not obj[4]:
                with transaction.atomic():
                    purchased = Order.objects.filter(
                        user=user, eventdetail__event_id=eventid, is_test=True).count()
                    if purchased >= user.customer.count:
                        return JsonResponse({'response_state': 400,
                                             'msg': '不可再次购买'})
                    order = Order.objects.create(user=user,
                                                 eventdetail_id=obj[0],
                                                 order_num=time.strftime
                                                 ('%Y%m%d%H%M%S'))
                    cursor.execute('UPDATE apt_eventdetail set is_testsold=%s \
                                    where id=%s' % (True, house))
                return JsonResponse(
                    {
                        'response_state': 200,
                        'room_info': ('%s-%s-%s-%s') % (obj[5],
                                                        obj[6],
                                                        obj[7],
                                                        obj[8]),
                        'limit': (
                            order.time + timedelta(
                                hours=event.limit)).strftime('%Y年%m月%d日 %H:%M:%S'),
                        'ordertime': order.time,
                        'orderid': order.id,
                    })
            elif Order.objects.filter(user=user, eventdetail_id=obj[0],
                                      is_test=True).exists():
                return JsonResponse({'response_state': 400,
                                     'msg': '已购买,不要重复购买'})
        elif (now >= event.event_start) and (now <= event.event_end):
            if not obj[1] and not obj[2]:
                with transaction.atomic():
                    purchased = Order.objects.filter(
                        user=user, eventdetail__event_id=eventid, is_test=False).count()
                    if purchased >= user.customer.count:
                        return JsonResponse({'response_state': 400,
                                             'msg': '不可再次购买'})
                    order = Order.objects.create(user=user,
                                                 eventdetail_id=obj[0],
                                                 order_num=time.strftime
                                                 ('%Y%m%d%H%M%S'),
                                                 is_test=False)
                    cursor.execute('UPDATE apt_eventdetail set is_sold=%s \
                                    where id=%s' % (True, house))
                return JsonResponse(
                    {
                        'response_state': 200,
                        'room_info': ('%s-%s-%s-%s') % (obj[5],
                                                        obj[6],
                                                        obj[7],
                                                        obj[8]),
                        'limit': (
                            order.time + timedelta(
                                hours=event.limit)).strftime('%Y年%m月%d日 %H:%M:%S'),
                        'ordertime': order.time,
                        'orderid': order.id,
                    })
            elif not obj[1] and obj[2]:
                cursor.execute(
                    'UPDATE apt_eventdetail set is_sold=%s where id=%s' %
                    (True, house))
                return JsonResponse(
                    {'response_state': 400, 'msg': '购买失败，房屋已卖出'})
            elif Order.objects.filter(user=user, eventdetail_id=obj[0],
                                      is_test=False).exists():
                return JsonResponse({'response_state': 400,
                                     'msg': '已购买,不要重复购买'})
        return JsonResponse({'response_state': 400, 'msg': '购买失败'})


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class OrderProView(View):
    '''
    订单中协议
    '''

    def get(self, request):
        user = request.user
        eventid = request.GET.get('id')
        try:
            customer = Customer.objects.get(
                use=user, event_id=eventid)
        except BaseException:
            return JsonResponse({'response_state': 400, 'msg': '认筹名单中没有该用户！'})
        else:
            value = [{
                'termname': customer.event.termname,
                'term': customer.event.term,
            }]
            context = {}
            context['objects'] = value
            context['response_state'] = 200
            return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class AppOrderListView(View):
    '''
    订单列表
    '''

    def get(self, request):
        user = request.user
        eventid = request.GET.get('id')
        objs = Order.objects.filter(user=user, eventdetail__event_id=eventid)
        valuelist = []
        for obj in objs:
            value = [{
                'order_num': obj.order_num,
                'room_info': (
                    obj.eventdetail.building +
                    obj.eventdetail.unit +
                    str(obj.eventdetail.floor) + '层' +
                    str(obj.eventdetail.room_num)),
                'time': obj.time.strftime('%Y/%m/%d %H:%M:%S'),
                'event': obj.eventdetail.event.name,
                'unit_price': obj.eventdetail.unit_price if obj.eventdetail.event.covered_space_price else '',
                'orderid': obj.id,
            }]
            valuelist.append(value)
        context = {}
        context['objects'] = valuelist
        context['response_state'] = 200
        return JsonResponse(context)


@method_decorator(customer_login_required, name='dispatch')
@method_decorator(customer_login_time, name='dispatch')
class AppOrderInfoView(View):
    '''
    订单详情
    '''

    def get(self, request):
        orderid = request.GET.get('orderId')
        try:
            obj = Order.get(orderid)
        except BaseException:
            return JsonResponse({'response_state': 400, 'msg': '没有找到该订单！'})
        else:
            try:
                house_type = obj.eventdetail.house_type.name
            except BaseException:
                house_type = ''
            value = [
                {
                    'eventname': obj.eventdetail.event.name,
                    'unit_price': obj.eventdetail.unit_price,
                    'limit': (
                        obj.time +
                        timedelta(
                            hours=obj.eventdetail.event.limit)).strftime('%Y-%m-%d %H:%M:%S'),
                    'ordertime': obj.time.strftime('%Y/%m/%d %H:%M:%S'),
                    'room_info': (
                        obj.eventdetail.building +
                        obj.eventdetail.unit +
                        str(
                            obj.eventdetail.floor) + '层' +
                        str(
                            obj.eventdetail.room_num)),
                    'houst_type': house_type,
                    'area': obj.eventdetail.area,
                    'customer': obj.user.customer.realname,
                    'mobile': obj.user.customer.mobile,
                    'identication': obj.user.customer.identication,
                    'order_num': obj.order_num,
                    'total': (
                                (obj.eventdetail.area) *
                                (
                                    obj.eventdetail.unit_price))}]
        context = {}
        context['objects'] = value
        context['response_state'] = 200
        return JsonResponse(context)
